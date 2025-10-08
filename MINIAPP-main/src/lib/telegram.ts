import WebApp from '@twa-dev/sdk';

export interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
  is_premium?: boolean;
}

class TelegramService {
  private webApp = WebApp;

  init() {
    this.webApp.ready();
    this.webApp.expand();
    this.setHeaderColor();
  }

  setHeaderColor(color: string = '#ffffff') {
    this.webApp.setHeaderColor(color);
  }

  setBackgroundColor(color: string = '#ffffff') {
    this.webApp.setBackgroundColor(color);
  }

  getUser(): TelegramUser | null {
    const user = this.webApp.initDataUnsafe?.user;
    if (!user) return null;

    return {
      id: user.id,
      first_name: user.first_name,
      last_name: user.last_name,
      username: user.username,
      language_code: user.language_code,
      is_premium: user.is_premium,
    };
  }

  showAlert(message: string) {
    this.webApp.showAlert(message);
  }

  showConfirm(message: string): Promise<boolean> {
    return new Promise((resolve) => {
      this.webApp.showConfirm(message, resolve);
    });
  }

  close() {
    this.webApp.close();
  }

  enableClosingConfirmation() {
    this.webApp.enableClosingConfirmation();
  }

  disableClosingConfirmation() {
    this.webApp.disableClosingConfirmation();
  }

  get colorScheme() {
    return this.webApp.colorScheme;
  }

  get themeParams() {
    return this.webApp.themeParams;
  }

  onThemeChanged(callback: () => void) {
    this.webApp.onEvent('themeChanged', callback);
  }

  get isExpanded() {
    return this.webApp.isExpanded;
  }

  get platform() {
    return this.webApp.platform;
  }
}

export const telegram = new TelegramService();
