import { invoke } from '@tauri-apps/api/core';
import { AnonymizerConfig, AnonymizationResult } from './types';

export const tauriApi = {
  async anonymizeText(text: string, config: AnonymizerConfig): Promise<AnonymizationResult> {
    return await invoke('anonymize_text', { text, config });
  },

  async deanonymizeText(text: string, config: AnonymizerConfig): Promise<AnonymizationResult> {
    return await invoke('deanonymize_text', { text, config });
  },

  async saveConfig(config: AnonymizerConfig): Promise<string> {
    return await invoke('save_config', { config });
  },

  async loadConfig(configName: string): Promise<AnonymizerConfig> {
    return await invoke('load_config', { configName });
  },

  async listConfigs(): Promise<string[]> {
    return await invoke('list_configs');
  },

  async deleteConfig(configName: string): Promise<string> {
    return await invoke('delete_config', { configName });
  },

  async createSampleConfig(): Promise<string> {
    return await invoke('create_sample_config');
  },
}; 