use std::path::PathBuf;
use serde::{Deserialize, Serialize};
use regex::Regex;
use anyhow::{Result, anyhow};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReplacementRule {
    pub original: String,
    pub replacement: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnonymizerConfig {
    pub config_name: String,
    pub case_insensitive: bool,
    pub whole_words_only: bool,
    pub replacements: Vec<ReplacementRule>,
    pub created_date: String,
    pub last_modified: String,
}

impl Default for AnonymizerConfig {
    fn default() -> Self {
        let now = chrono::Utc::now().format("%Y-%m-%d").to_string();
        Self {
            config_name: "Default".to_string(),
            case_insensitive: false,
            whole_words_only: true,
            replacements: Vec::new(),
            created_date: now.clone(),
            last_modified: now,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AnonymizationResult {
    pub success: bool,
    pub message: String,
    pub text: Option<String>,
}

// Helper function to get configs directory
fn get_configs_dir() -> Result<PathBuf> {
    let home_dir = dirs::home_dir().ok_or_else(|| anyhow!("Could not find home directory"))?;
    let config_dir = home_dir.join(".text-anonymizer").join("configs");
    std::fs::create_dir_all(&config_dir)?;
    Ok(config_dir)
}

// Helper function to preserve case pattern
fn preserve_case_pattern(original_match: &str, replacement: &str) -> String {
    if original_match.is_empty() {
        return replacement.to_string();
    }

    let mut result = String::new();
    let replacement_chars: Vec<char> = replacement.chars().collect();
    let original_chars: Vec<char> = original_match.chars().collect();

    for (i, &replacement_char) in replacement_chars.iter().enumerate() {
        if i < original_chars.len() {
            if original_chars[i].is_uppercase() {
                result.push(replacement_char.to_uppercase().collect::<String>().chars().next().unwrap_or(replacement_char));
            } else {
                result.push(replacement_char.to_lowercase().collect::<String>().chars().next().unwrap_or(replacement_char));
            }
        } else {
            result.push(replacement_char.to_lowercase().collect::<String>().chars().next().unwrap_or(replacement_char));
        }
    }

    result
}

#[tauri::command]
async fn anonymize_text(text: String, config: AnonymizerConfig) -> Result<AnonymizationResult, String> {
    if text.is_empty() {
        return Ok(AnonymizationResult {
            success: false,
            message: "Please enter text to anonymize.".to_string(),
            text: None,
        });
    }

    let mut anonymized_text = text;

    for rule in &config.replacements {
        let original = &rule.original;
        let replacement = &rule.replacement;

        if config.case_insensitive {
            // Create regex pattern
            let pattern = if config.whole_words_only {
                format!(r"\b{}\b", regex::escape(original))
            } else {
                regex::escape(original)
            };

            match Regex::new(&format!("(?i){}", pattern)) {
                Ok(re) => {
                    anonymized_text = re.replace_all(&anonymized_text, |caps: &regex::Captures| {
                        let matched_text = &caps[0];
                        preserve_case_pattern(matched_text, replacement)
                    }).to_string();
                }
                Err(e) => {
                    return Ok(AnonymizationResult {
                        success: false,
                        message: format!("Regex error: {}", e),
                        text: None,
                    });
                }
            }
        } else {
            // Case-sensitive replacement
            if config.whole_words_only {
                let pattern = format!(r"\b{}\b", regex::escape(original));
                match Regex::new(&pattern) {
                    Ok(re) => {
                        anonymized_text = re.replace_all(&anonymized_text, replacement).to_string();
                    }
                    Err(e) => {
                        return Ok(AnonymizationResult {
                            success: false,
                            message: format!("Regex error: {}", e),
                            text: None,
                        });
                    }
                }
            } else {
                anonymized_text = anonymized_text.replace(original, replacement);
            }
        }
    }

    Ok(AnonymizationResult {
        success: true,
        message: "Text anonymized successfully! 🔒".to_string(),
        text: Some(anonymized_text),
    })
}

#[tauri::command]
async fn deanonymize_text(text: String, config: AnonymizerConfig) -> Result<AnonymizationResult, String> {
    if text.is_empty() {
        return Ok(AnonymizationResult {
            success: false,
            message: "Please enter text to de-anonymize.".to_string(),
            text: None,
        });
    }

    let mut deanonymized_text = text;

    // Apply reverse replacements
    for rule in config.replacements.iter().rev() {
        let original = &rule.original;
        let replacement = &rule.replacement;

        if config.case_insensitive {
            // Create regex pattern
            let pattern = if config.whole_words_only {
                format!(r"\b{}\b", regex::escape(replacement))
            } else {
                regex::escape(replacement)
            };

            match Regex::new(&format!("(?i){}", pattern)) {
                Ok(re) => {
                    deanonymized_text = re.replace_all(&deanonymized_text, |caps: &regex::Captures| {
                        let matched_text = &caps[0];
                        preserve_case_pattern(matched_text, original)
                    }).to_string();
                }
                Err(e) => {
                    return Ok(AnonymizationResult {
                        success: false,
                        message: format!("Regex error: {}", e),
                        text: None,
                    });
                }
            }
        } else {
            // Case-sensitive replacement
            if config.whole_words_only {
                let pattern = format!(r"\b{}\b", regex::escape(replacement));
                match Regex::new(&pattern) {
                    Ok(re) => {
                        deanonymized_text = re.replace_all(&deanonymized_text, original).to_string();
                    }
                    Err(e) => {
                        return Ok(AnonymizationResult {
                            success: false,
                            message: format!("Regex error: {}", e),
                            text: None,
                        });
                    }
                }
            } else {
                deanonymized_text = deanonymized_text.replace(replacement, original);
            }
        }
    }

    Ok(AnonymizationResult {
        success: true,
        message: "Text de-anonymized successfully! 🔓".to_string(),
        text: Some(deanonymized_text),
    })
}

#[tauri::command]
async fn save_config(config: AnonymizerConfig) -> Result<String, String> {
    let configs_dir = get_configs_dir().map_err(|e| e.to_string())?;
    let filename = configs_dir.join(format!("config_{}.json", config.config_name));
    
    let mut config_to_save = config;
    config_to_save.last_modified = chrono::Utc::now().format("%Y-%m-%d").to_string();
    
    let json_content = serde_json::to_string_pretty(&config_to_save)
        .map_err(|e| format!("Failed to serialize config: {}", e))?;
    
    std::fs::write(&filename, json_content)
        .map_err(|e| format!("Failed to write config file: {}", e))?;
    
    Ok("Configuration saved successfully!".to_string())
}

#[tauri::command]
async fn load_config(config_name: String) -> Result<AnonymizerConfig, String> {
    let configs_dir = get_configs_dir().map_err(|e| e.to_string())?;
    let filename = configs_dir.join(format!("config_{}.json", config_name));
    
    if !filename.exists() {
        return Err(format!("Configuration '{}' not found", config_name));
    }
    
    let json_content = std::fs::read_to_string(&filename)
        .map_err(|e| format!("Failed to read config file: {}", e))?;
    
    let config: AnonymizerConfig = serde_json::from_str(&json_content)
        .map_err(|e| format!("Failed to parse config file: {}", e))?;
    
    Ok(config)
}

#[tauri::command]
async fn list_configs() -> Result<Vec<String>, String> {
    let configs_dir = get_configs_dir().map_err(|e| e.to_string())?;
    
    let mut config_names = Vec::new();
    
    if let Ok(entries) = std::fs::read_dir(&configs_dir) {
        for entry in entries {
            if let Ok(entry) = entry {
                let path = entry.path();
                if let Some(filename) = path.file_name() {
                    if let Some(filename_str) = filename.to_str() {
                        if filename_str.starts_with("config_") && filename_str.ends_with(".json") {
                            let config_name = filename_str
                                .strip_prefix("config_")
                                .unwrap()
                                .strip_suffix(".json")
                                .unwrap()
                                .to_string();
                            config_names.push(config_name);
                        }
                    }
                }
            }
        }
    }
    
    config_names.sort();
    Ok(config_names)
}

#[tauri::command]
async fn delete_config(config_name: String) -> Result<String, String> {
    let configs_dir = get_configs_dir().map_err(|e| e.to_string())?;
    let filename = configs_dir.join(format!("config_{}.json", config_name));
    
    if !filename.exists() {
        return Err(format!("Configuration '{}' not found", config_name));
    }
    
    std::fs::remove_file(&filename)
        .map_err(|e| format!("Failed to delete config file: {}", e))?;
    
    Ok(format!("Configuration '{}' deleted successfully!", config_name))
}

#[tauri::command]
async fn create_sample_config() -> Result<String, String> {
    let sample_config = AnonymizerConfig {
        config_name: "Sample".to_string(),
        case_insensitive: true,
        whole_words_only: true,
        replacements: vec![
            ReplacementRule {
                original: "CompanyName Inc.".to_string(),
                replacement: "COMPANY_ANONYMOUS".to_string(),
            },
            ReplacementRule {
                original: "john.doe@company.com".to_string(),
                replacement: "user1@example.com".to_string(),
            },
            ReplacementRule {
                original: "table_production_data".to_string(),
                replacement: "table_generic_data".to_string(),
            },
            ReplacementRule {
                original: "api_key_12345".to_string(),
                replacement: "API_KEY_HIDDEN".to_string(),
            },
            ReplacementRule {
                original: "David".to_string(),
                replacement: "Lucas".to_string(),
            },
            ReplacementRule {
                original: "Microsoft".to_string(),
                replacement: "TECH_COMPANY".to_string(),
            },
        ],
        created_date: chrono::Utc::now().format("%Y-%m-%d").to_string(),
        last_modified: chrono::Utc::now().format("%Y-%m-%d").to_string(),
    };
    
    save_config(sample_config).await
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_fs::init())
        .invoke_handler(tauri::generate_handler![
            anonymize_text,
            deanonymize_text,
            save_config,
            load_config,
            list_configs,
            delete_config,
            create_sample_config
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
