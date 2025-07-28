export interface ReplacementRule {
  original: string;
  replacement: string;
}

export interface AnonymizerConfig {
  config_name: string;
  case_insensitive: boolean;
  whole_words_only: boolean;
  replacements: ReplacementRule[];
  created_date: string;
  last_modified: string;
}

export interface AnonymizationResult {
  success: boolean;
  message: string;
  text?: string;
}

export const createDefaultConfig = (): AnonymizerConfig => ({
  config_name: "Default",
  case_insensitive: false,
  whole_words_only: true,
  replacements: [],
  created_date: new Date().toISOString().split('T')[0],
  last_modified: new Date().toISOString().split('T')[0],
}); 