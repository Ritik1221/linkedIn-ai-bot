/**
 * Secure storage utility for the LinkedIn AI Agent.
 * This utility provides methods for storing data securely in client-side storage.
 */

/**
 * Simple encryption function for client-side data
 * Note: This is not cryptographically secure, but provides basic protection
 * For truly sensitive data, use server-side storage and HTTPS
 */
const encrypt = (text: string): string => {
  if (!text) return '';
  
  try {
    // Base64 encode the string (simple obfuscation)
    const encodedText = Buffer.from(text).toString('base64');
    
    // Add timestamp and a simple scramble
    const timestamp = Date.now().toString();
    const scrambledText = encodedText.split('').reverse().join('');
    
    // Combine timestamp and scrambled text, then encode again
    return Buffer.from(`${timestamp}:${scrambledText}`).toString('base64');
  } catch (error) {
    console.error('Encryption failed:', error);
    return '';
  }
};

/**
 * Simple decryption function for client-side data
 * Reverses the encrypt function
 */
const decrypt = (encryptedText: string): string => {
  if (!encryptedText) return '';
  
  try {
    // Decode base64
    const decodedText = Buffer.from(encryptedText, 'base64').toString();
    
    // Split timestamp and scrambled text
    const [timestamp, scrambledText] = decodedText.split(':');
    
    // Unscramble text
    const encodedText = scrambledText.split('').reverse().join('');
    
    // Decode final text
    return Buffer.from(encodedText, 'base64').toString();
  } catch (error) {
    console.error('Decryption failed:', error);
    return '';
  }
};

/**
 * Secure storage utility
 */
export const secureStorage = {
  /**
   * Set item in secure storage
   * @param key Storage key
   * @param value Value to store
   */
  setItem: (key: string, value: any): void => {
    if (!key || value === undefined) return;
    
    try {
      const encryptedValue = encrypt(JSON.stringify(value));
      sessionStorage.setItem(key, encryptedValue);
    } catch (error) {
      console.error(`Failed to store ${key}:`, error);
    }
  },
  
  /**
   * Get item from secure storage
   * @param key Storage key
   * @returns Stored value or null if not found
   */
  getItem: <T>(key: string): T | null => {
    if (!key) return null;
    
    try {
      const encryptedValue = sessionStorage.getItem(key);
      if (!encryptedValue) return null;
      
      const decryptedValue = decrypt(encryptedValue);
      return JSON.parse(decryptedValue) as T;
    } catch (error) {
      console.error(`Failed to retrieve ${key}:`, error);
      return null;
    }
  },
  
  /**
   * Remove item from secure storage
   * @param key Storage key
   */
  removeItem: (key: string): void => {
    if (!key) return;
    
    try {
      sessionStorage.removeItem(key);
    } catch (error) {
      console.error(`Failed to remove ${key}:`, error);
    }
  },
  
  /**
   * Clear all items from secure storage
   */
  clear: (): void => {
    try {
      sessionStorage.clear();
    } catch (error) {
      console.error('Failed to clear storage:', error);
    }
  },
};

export default secureStorage; 