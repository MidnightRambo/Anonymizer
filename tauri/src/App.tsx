import React, { useState, useEffect } from 'react';
import { 
  Lock, 
  Unlock, 
  Copy, 
  Trash2, 
  Plus, 
  Edit, 
  Save, 
  FolderOpen, 
  FileText,
  AlertCircle,
  CheckCircle,
  X
} from 'lucide-react';
import './App.css';
import { AnonymizerConfig, ReplacementRule, createDefaultConfig } from './types';
import { tauriApi } from './tauri-api';

interface Message {
  type: 'success' | 'error' | 'warning';
  text: string;
}

function App() {
  const [text, setText] = useState('');
  const [config, setConfig] = useState<AnonymizerConfig>(createDefaultConfig());
  const [availableConfigs, setAvailableConfigs] = useState<string[]>([]);
  const [selectedRule, setSelectedRule] = useState<number>(-1);
  const [originalText, setOriginalText] = useState('');
  const [replacementText, setReplacementText] = useState('');
  const [message, setMessage] = useState<Message | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Enable dark mode
    document.documentElement.classList.add('dark');
    loadAvailableConfigs();
    initializeSampleConfig();
  }, []);

  const initializeSampleConfig = async () => {
    try {
      await tauriApi.createSampleConfig();
      await loadAvailableConfigs();
    } catch (error) {
      console.error('Error creating sample config:', error);
    }
  };

  const loadAvailableConfigs = async () => {
    try {
      const configs = await tauriApi.listConfigs();
      setAvailableConfigs(configs);
      if (configs.length > 0 && !configs.includes(config.config_name)) {
        await loadConfigByName(configs[0]);
      }
    } catch (error) {
      showMessage('error', 'Failed to load configurations');
    }
  };

  const loadConfigByName = async (configName: string) => {
    try {
      const loadedConfig = await tauriApi.loadConfig(configName);
      setConfig(loadedConfig);
      clearRuleForm();
    } catch (error) {
      showMessage('error', `Failed to load configuration: ${configName}`);
    }
  };

  const showMessage = (type: 'success' | 'error' | 'warning', text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 5000);
  };

  const anonymizeText = async () => {
    if (!text.trim()) {
      showMessage('warning', 'Please enter text to anonymize.');
      return;
    }

    setIsLoading(true);
    try {
      const result = await tauriApi.anonymizeText(text, config);
      if (result.success && result.text) {
        setText(result.text);
        showMessage('success', result.message);
      } else {
        showMessage('error', result.message);
      }
    } catch (error) {
      showMessage('error', 'Failed to anonymize text');
    } finally {
      setIsLoading(false);
    }
  };

  const deanonymizeText = async () => {
    if (!text.trim()) {
      showMessage('warning', 'Please enter text to de-anonymize.');
      return;
    }

    setIsLoading(true);
    try {
      const result = await tauriApi.deanonymizeText(text, config);
      if (result.success && result.text) {
        setText(result.text);
        showMessage('success', result.message);
      } else {
        showMessage('error', result.message);
      }
    } catch (error) {
      showMessage('error', 'Failed to de-anonymize text');
    } finally {
      setIsLoading(false);
    }
  };

  const saveConfiguration = async () => {
    if (!config.config_name.trim()) {
      showMessage('warning', 'Please enter a configuration name.');
      return;
    }

    setIsLoading(true);
    try {
      const message = await tauriApi.saveConfig(config);
      showMessage('success', message);
      await loadAvailableConfigs();
    } catch (error) {
      showMessage('error', 'Failed to save configuration');
    } finally {
      setIsLoading(false);
    }
  };

  const deleteConfiguration = async () => {
    if (!config.config_name || !availableConfigs.includes(config.config_name)) {
      showMessage('warning', 'Please select a configuration to delete.');
      return;
    }

    if (!confirm(`Are you sure you want to delete configuration '${config.config_name}'?`)) {
      return;
    }

    setIsLoading(true);
    try {
      const message = await tauriApi.deleteConfig(config.config_name);
      showMessage('success', message);
      setConfig(createDefaultConfig());
      await loadAvailableConfigs();
    } catch (error) {
      showMessage('error', 'Failed to delete configuration');
    } finally {
      setIsLoading(false);
    }
  };

  const addRule = () => {
    if (!originalText.trim() || !replacementText.trim()) {
      showMessage('warning', 'Both original and replacement text are required.');
      return;
    }

    // Check for duplicates
    if (config.replacements.some(rule => rule.original === originalText)) {
      showMessage('warning', 'Rule with this original text already exists.');
      return;
    }

    const newRule: ReplacementRule = {
      original: originalText,
      replacement: replacementText,
    };

    setConfig(prev => ({
      ...prev,
      replacements: [...prev.replacements, newRule],
      last_modified: new Date().toISOString().split('T')[0],
    }));

    clearRuleForm();
    showMessage('success', 'Rule added successfully');
  };

  const updateRule = () => {
    if (selectedRule < 0) {
      showMessage('warning', 'Please select a rule to update.');
      return;
    }

    if (!originalText.trim() || !replacementText.trim()) {
      showMessage('warning', 'Both original and replacement text are required.');
      return;
    }

    // Check for duplicates (excluding current rule)
    const existingRule = config.replacements.find(
      (rule, index) => rule.original === originalText && index !== selectedRule
    );
    if (existingRule) {
      showMessage('warning', 'Rule with this original text already exists.');
      return;
    }

    setConfig(prev => ({
      ...prev,
      replacements: prev.replacements.map((rule, index) =>
        index === selectedRule
          ? { original: originalText, replacement: replacementText }
          : rule
      ),
      last_modified: new Date().toISOString().split('T')[0],
    }));

    clearRuleForm();
    showMessage('success', 'Rule updated successfully');
  };

  const removeRule = () => {
    if (selectedRule < 0) {
      showMessage('warning', 'Please select a rule to remove.');
      return;
    }

    setConfig(prev => ({
      ...prev,
      replacements: prev.replacements.filter((_, index) => index !== selectedRule),
      last_modified: new Date().toISOString().split('T')[0],
    }));

    clearRuleForm();
    showMessage('success', 'Rule removed successfully');
  };

  const selectRule = (index: number) => {
    setSelectedRule(index);
    const rule = config.replacements[index];
    setOriginalText(rule.original);
    setReplacementText(rule.replacement);
  };

  const clearRuleForm = () => {
    setSelectedRule(-1);
    setOriginalText('');
    setReplacementText('');
  };

  const clearText = () => {
    setText('');
  };

  const copyToClipboard = async () => {
    if (!text.trim()) {
      showMessage('warning', 'No text to copy.');
      return;
    }

    try {
      await navigator.clipboard.writeText(text);
      showMessage('success', 'Text copied to clipboard! 📋');
    } catch (error) {
      showMessage('error', 'Failed to copy to clipboard');
    }
  };

  const newConfiguration = () => {
    setConfig(createDefaultConfig());
    clearRuleForm();
  };

  // Handle Tab key in textarea to insert tab character instead of focusing next element
  const handleTextareaKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.target as HTMLTextAreaElement;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      const newText = text.substring(0, start) + '\t' + text.substring(end);
      setText(newText);
      
      // Set cursor position after the inserted tab
      setTimeout(() => {
        target.selectionStart = target.selectionEnd = start + 1;
      }, 0);
    }
  };

  const MessageComponent = ({ message, onClose }: { message: Message; onClose: () => void }) => (
    <div className={`fixed top-4 right-4 z-50 flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg transition-all duration-300 ${
      message.type === 'success' ? 'bg-dark-success text-white' :
      message.type === 'error' ? 'bg-dark-danger text-white' :
      'bg-dark-warning text-white'
    }`}>
      {message.type === 'success' && <CheckCircle size={20} />}
      {message.type === 'error' && <AlertCircle size={20} />}
      {message.type === 'warning' && <AlertCircle size={20} />}
      <span>{message.text}</span>
      <button onClick={onClose} className="ml-2 hover:opacity-70">
        <X size={16} />
      </button>
    </div>
  );

  return (
    <div className="h-screen bg-dark-bg overflow-hidden">
      {message && <MessageComponent message={message} onClose={() => setMessage(null)} />}
      
      <div className="w-full h-full flex flex-col overflow-x-auto">
        <div className="h-full flex flex-col p-2 sm:p-3">
          <h1 className="text-lg sm:text-xl lg:text-2xl font-bold text-dark-text mb-2 sm:mb-3 text-center flex-shrink-0">
            Text Anonymization Tool - 2025 Edition
          </h1>
          
          {/* Ultra-compact main content area that fits in viewport and expands fully */}
          <div className="flex flex-col xl:flex-row gap-2 sm:gap-3 w-full flex-1">
            {/* Text Processing Panel - Expands fully on wide screens */}
            <div className="flex-1 xl:flex-[2] flex flex-col">
              <div className="modern-card flex-1 flex flex-col">
                <h2 className="text-sm sm:text-base font-semibold text-dark-text mb-2 flex-shrink-0">Text Processing</h2>
                
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  onKeyDown={handleTextareaKeyDown}
                  className="modern-textarea w-full flex-1 text-xs sm:text-sm"
                  placeholder="Enter your text here to anonymize or de-anonymize..."
                  disabled={isLoading}
                />
                
                <div className="flex flex-wrap gap-1 sm:gap-2 mt-2 flex-shrink-0">
                  <button
                    onClick={anonymizeText}
                    disabled={isLoading}
                    className="modern-button-primary flex items-center gap-1 text-xs px-2 py-1 flex-shrink-0"
                  >
                    <Lock size={12} />
                    {isLoading ? 'Processing...' : 'Anonymize'}
                  </button>
                  
                  <button
                    onClick={deanonymizeText}
                    disabled={isLoading}
                    className="modern-button-secondary flex items-center gap-1 text-xs px-2 py-1 flex-shrink-0"
                  >
                    <Unlock size={12} />
                    De-anonymize
                  </button>
                  
                  <button
                    onClick={clearText}
                    className="modern-button-secondary flex items-center gap-1 text-xs px-2 py-1 flex-shrink-0"
                  >
                    <Trash2 size={12} />
                    Clear
                  </button>
                  
                  <button
                    onClick={copyToClipboard}
                    className="modern-button-secondary flex items-center gap-1 text-xs px-2 py-1 flex-shrink-0"
                  >
                    <Copy size={12} />
                    Copy
                  </button>
                </div>
              </div>
            </div>
            
            {/* Configuration Panel - Expands fully on wide screens */}
            <div className="flex-1 xl:flex-[1] flex flex-col">
              <div className="flex flex-col gap-2 h-full">
                {/* Configuration Selector - Minimal spacing */}
                <div className="modern-card flex-shrink-0">
                  <h3 className="text-xs sm:text-sm font-semibold text-dark-text mb-2">Configuration</h3>
                  
                  <div className="space-y-2">
                    <div>
                      <label className="block text-xs font-medium text-dark-text mb-1">
                        Active:
                      </label>
                      <select
                        value={config.config_name}
                        onChange={(e) => loadConfigByName(e.target.value)}
                        className="modern-select w-full text-xs"
                      >
                        {availableConfigs.map(configName => (
                          <option key={configName} value={configName}>
                            {configName}
                          </option>
                        ))}
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-xs font-medium text-dark-text mb-1">
                        Name:
                      </label>
                      <input
                        type="text"
                        value={config.config_name}
                        onChange={(e) => setConfig(prev => ({ ...prev, config_name: e.target.value }))}
                        className="modern-input w-full text-xs"
                      />
                    </div>
                    
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      <div>
                        <label className="block text-xs font-medium text-dark-text mb-1">
                          Case:
                        </label>
                        <select
                          value={config.case_insensitive ? 'insensitive' : 'sensitive'}
                          onChange={(e) => setConfig(prev => ({ 
                            ...prev, 
                            case_insensitive: e.target.value === 'insensitive' 
                          }))}
                          className="modern-select w-full text-xs"
                        >
                          <option value="sensitive">Sensitive</option>
                          <option value="insensitive">Insensitive</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-xs font-medium text-dark-text mb-1">
                          Words:
                        </label>
                        <select
                          value={config.whole_words_only ? 'whole' : 'anywhere'}
                          onChange={(e) => setConfig(prev => ({ 
                            ...prev, 
                            whole_words_only: e.target.value === 'whole' 
                          }))}
                          className="modern-select w-full text-xs"
                        >
                          <option value="whole">Whole only</option>
                          <option value="anywhere">Anywhere</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Replacement Rules - Flexible height, ultra-compact */}
                <div className="modern-card flex-1 flex flex-col">
                  <h3 className="text-xs sm:text-sm font-semibold text-dark-text mb-2 flex-shrink-0">Replacement Rules</h3>
                  
                  {/* Scrollable Rules Table Container - Maximized available space */}
                  <div className="bg-dark-surface border border-dark-border rounded-lg overflow-hidden mb-2 flex-1 overflow-y-auto">
                    <table className="modern-table w-full">
                      <thead className="sticky top-0 z-10">
                        <tr>
                          <th className="px-2 py-1 text-xs w-1/2">Original</th>
                          <th className="px-2 py-1 text-xs w-1/2">Replacement</th>
                        </tr>
                      </thead>
                      <tbody>
                        {config.replacements.map((rule, index) => (
                          <tr
                            key={index}
                            onClick={() => selectRule(index)}
                            className={`cursor-pointer ${index === selectedRule ? 'selected' : ''}`}
                          >
                            <td className="px-2 py-1 text-xs truncate w-1/2" title={rule.original}>{rule.original}</td>
                            <td className="px-2 py-1 text-xs truncate w-1/2" title={rule.replacement}>{rule.replacement}</td>
                          </tr>
                        ))}
                        {config.replacements.length === 0 && (
                          <tr>
                            <td colSpan={2} className="text-center text-dark-textSecondary py-4 text-xs">
                              No rules defined. Add some rules to get started.
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                  
                  {/* Rule Form - Ultra-compact form */}
                  <div className="space-y-1 flex-shrink-0">
                    <div>
                      <label className="block text-xs font-medium text-dark-text mb-1">
                        Original:
                      </label>
                      <input
                        type="text"
                        value={originalText}
                        onChange={(e) => setOriginalText(e.target.value)}
                        className="modern-input w-full text-xs"
                        placeholder="Text to replace..."
                      />
                    </div>
                    
                    <div>
                      <label className="block text-xs font-medium text-dark-text mb-1">
                        Replacement:
                      </label>
                      <input
                        type="text"
                        value={replacementText}
                        onChange={(e) => setReplacementText(e.target.value)}
                        className="modern-input w-full text-xs"
                        placeholder="Replacement text..."
                      />
                    </div>
                    
                    <div className="flex gap-1 flex-wrap">
                      <button
                        onClick={addRule}
                        className="modern-button-primary flex items-center gap-1 text-xs px-2 py-1 flex-shrink-0"
                      >
                        <Plus size={10} />
                        <span className="hidden sm:inline">Add</span>
                      </button>
                      
                      <button
                        onClick={updateRule}
                        className="modern-button-secondary flex items-center gap-1 text-xs px-2 py-1 flex-shrink-0"
                      >
                        <Edit size={10} />
                        <span className="hidden sm:inline">Update</span>
                      </button>
                      
                      <button
                        onClick={removeRule}
                        className="modern-button-danger flex items-center gap-1 text-xs px-2 py-1 flex-shrink-0"
                      >
                        <Trash2 size={10} />
                        <span className="hidden sm:inline">Remove</span>
                      </button>
                    </div>
                  </div>
                </div>
                
                {/* Configuration Management - Minimal fixed height */}
                <div className="modern-card flex-shrink-0">
                  <h3 className="text-xs sm:text-sm font-semibold text-dark-text mb-2">Config Management</h3>
                  
                  <div className="grid grid-cols-2 xl:grid-cols-4 gap-1">
                    <button
                      onClick={newConfiguration}
                      className="modern-button-secondary flex items-center gap-1 justify-center text-xs px-2 py-1"
                    >
                      <FileText size={10} />
                      <span className="truncate hidden sm:inline">New</span>
                    </button>
                    
                    <button
                      onClick={() => {/* Load from file logic */}}
                      className="modern-button-secondary flex items-center gap-1 justify-center text-xs px-2 py-1"
                    >
                      <FolderOpen size={10} />
                      <span className="truncate hidden sm:inline">Load</span>
                    </button>
                    
                    <button
                      onClick={saveConfiguration}
                      disabled={isLoading}
                      className="modern-button-primary flex items-center gap-1 justify-center text-xs px-2 py-1"
                    >
                      <Save size={10} />
                      <span className="truncate hidden sm:inline">Save</span>
                    </button>
                    
                    <button
                      onClick={deleteConfiguration}
                      disabled={isLoading}
                      className="modern-button-danger flex items-center gap-1 justify-center text-xs px-2 py-1"
                    >
                      <Trash2 size={10} />
                      <span className="truncate hidden sm:inline">Delete</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 