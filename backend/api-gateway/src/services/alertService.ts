import { Resend } from 'resend';
import { logger } from '../utils/logger';
import { RedisService } from './redisService';

interface Alert {
  id: string;
  userId: string;
  symbol: string;
  type: 'price' | 'recommendation' | 'news';
  message: string;
  priority: 'low' | 'medium' | 'high';
  timestamp: Date;
  read: boolean;
}

interface EmailAlert {
  to: string;
  symbol: string;
  action: 'BUY' | 'SELL' | 'HOLD';
  riskTier: string;
  confidence: number;
  reasoning: string;
}

export class AlertService {
  private resend: Resend;
  private redis: RedisService;
  private emailTemplate: string;

  constructor() {
    const apiKey = process.env.RESEND_API_KEY;
    if (!apiKey) {
      throw new Error('RESEND_API_KEY environment variable is required');
    }
    
    this.resend = new Resend(apiKey);
    this.redis = new RedisService();
    this.emailTemplate = this.getEmailTemplate();
  }

  async initialize(): Promise<void> {
    try {
      await this.redis.connect();
      logger.info('✅ Alert Service initialized');
    } catch (error) {
      logger.error('❌ Failed to initialize Alert Service:', error);
      throw error;
    }
  }

  async sendEmailAlert(alertData: EmailAlert): Promise<void> {
    try {
      const { to, symbol, action, riskTier, confidence, reasoning } = alertData;

      // Check if user has email notifications enabled
      const notificationsEnabled = await this.redis.get(`notifications:${to}`);
      if (notificationsEnabled === 'false') {
        logger.info(`Email notifications disabled for ${to}`);
        return;
      }

      // Rate limiting - max 10 emails per hour per user
      const rateLimitKey = `email_rate_limit:${to}`;
      const currentCount = await this.redis.get(rateLimitKey);
      
      if (currentCount && parseInt(currentCount) >= 10) {
        logger.warn(`Rate limit exceeded for ${to}`);
        return;
      }

      const subject = `VUTAX Alert: ${action} ${symbol} - ${confidence}% Confidence`;
      const html = this.generateEmailHTML(symbol, action, riskTier, confidence, reasoning);

      const emailResult = await this.resend.emails.send({
        from: 'VUTAX Alerts <alerts@vutax.com>',
        to: [to],
        subject,
        html,
      });

      if (emailResult.error) {
        throw new Error(`Email send failed: ${emailResult.error.message}`);
      }

      // Update rate limiting
      await this.redis.incr(rateLimitKey);
      await this.redis.expire(rateLimitKey, 3600); // 1 hour

      logger.info(`✅ Email alert sent to ${to} for ${symbol}`);
    } catch (error) {
      logger.error('❌ Failed to send email alert:', error);
      throw error;
    }
  }

  async createAlert(alert: Omit<Alert, 'id' | 'timestamp'>): Promise<Alert> {
    try {
      const newAlert: Alert = {
        ...alert,
        id: this.generateAlertId(),
        timestamp: new Date(),
      };

      // Store in Redis
      await this.redis.setex(
        `alert:${newAlert.id}`,
        86400, // 24 hours
        JSON.stringify(newAlert)
      );

      // Add to user's alert list
      await this.redis.lpush(`user_alerts:${alert.userId}`, newAlert.id);
      await this.redis.ltrim(`user_alerts:${alert.userId}`, 0, 99); // Keep last 100 alerts

      logger.info(`✅ Alert created: ${newAlert.id}`);
      return newAlert;
    } catch (error) {
      logger.error('❌ Failed to create alert:', error);
      throw error;
    }
  }

  async getUserAlerts(userId: string, limit: number = 20): Promise<Alert[]> {
    try {
      const alertIds = await this.redis.lrange(`user_alerts:${userId}`, 0, limit - 1);
      const alerts: Alert[] = [];

      for (const alertId of alertIds) {
        const alertData = await this.redis.get(`alert:${alertId}`);
        if (alertData) {
          alerts.push(JSON.parse(alertData));
        }
      }

      return alerts.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
    } catch (error) {
      logger.error('❌ Failed to get user alerts:', error);
      throw error;
    }
  }

  async markAlertAsRead(alertId: string): Promise<void> {
    try {
      const alertData = await this.redis.get(`alert:${alertId}`);
      if (alertData) {
        const alert: Alert = JSON.parse(alertData);
        alert.read = true;
        await this.redis.setex(`alert:${alertId}`, 86400, JSON.stringify(alert));
      }
    } catch (error) {
      logger.error('❌ Failed to mark alert as read:', error);
      throw error;
    }
  }

  async toggleEmailNotifications(userId: string, enabled: boolean): Promise<void> {
    try {
      await this.redis.set(`notifications:${userId}`, enabled.toString());
      logger.info(`Email notifications ${enabled ? 'enabled' : 'disabled'} for ${userId}`);
    } catch (error) {
      logger.error('❌ Failed to toggle email notifications:', error);
      throw error;
    }
  }

  private generateEmailHTML(
    symbol: string,
    action: string,
    riskTier: string,
    confidence: number,
    reasoning: string
  ): string {
    const actionColor = action === 'BUY' ? '#22c55e' : action === 'SELL' ? '#ef4444' : '#64748b';
    const riskColor = riskTier === 'conservative' ? '#22c55e' : 
                     riskTier === 'regular' ? '#f59e0b' : '#ef4444';

    return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>VUTAX Stock Alert</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #334155; max-width: 600px; margin: 0 auto; padding: 20px;">
          
          <!-- Header -->
          <div style="text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
            <h1 style="margin: 0; font-size: 28px; font-weight: bold;">VUTAX</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">AI-Powered Stock Analysis</p>
          </div>

          <!-- Alert Content -->
          <div style="background: #f8fafc; border-radius: 12px; padding: 25px; margin-bottom: 20px; border-left: 4px solid ${actionColor};">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
              <h2 style="margin: 0; color: #1e293b; font-size: 24px;">${symbol}</h2>
              <span style="margin-left: 15px; padding: 4px 12px; background: ${actionColor}; color: white; border-radius: 20px; font-size: 14px; font-weight: bold;">${action}</span>
            </div>
            
            <div style="margin-bottom: 20px;">
              <div style="display: inline-block; margin-right: 20px;">
                <span style="color: #64748b; font-size: 14px;">Risk Tier:</span>
                <span style="margin-left: 5px; padding: 2px 8px; background: ${riskColor}; color: white; border-radius: 12px; font-size: 12px; text-transform: capitalize;">${riskTier}</span>
              </div>
              <div style="display: inline-block;">
                <span style="color: #64748b; font-size: 14px;">Confidence:</span>
                <span style="margin-left: 5px; font-weight: bold; color: #1e293b;">${confidence}%</span>
              </div>
            </div>

            <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
              <h4 style="margin: 0 0 10px 0; color: #374151; font-size: 16px;">Analysis:</h4>
              <p style="margin: 0; color: #4b5563; line-height: 1.5;">${reasoning}</p>
            </div>
          </div>

          <!-- Disclaimer -->
          <div style="background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 14px; color: #92400e;">
              <strong>⚠️ Important Disclaimer:</strong> This information is for educational purposes only and does not constitute financial advice. Always conduct your own research and consider your risk tolerance before making investment decisions.
            </p>
          </div>

          <!-- Footer -->
          <div style="text-align: center; padding-top: 20px; border-top: 1px solid #e2e8f0;">
            <p style="margin: 0; color: #64748b; font-size: 14px;">
              Generated by VUTAX AI at ${new Date().toLocaleString()}
            </p>
            <p style="margin: 10px 0 0 0; font-size: 12px; color: #94a3b8;">
              <a href="#" style="color: #667eea; text-decoration: none;">Manage Email Preferences</a> | 
              <a href="#" style="color: #667eea; text-decoration: none;">Unsubscribe</a>
            </p>
          </div>
        </body>
      </html>
    `;
  }

  private generateAlertId(): string {
    return `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private getEmailTemplate(): string {
    return `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2>VUTAX Stock Alert</h2>
        <p>{{message}}</p>
        <hr>
        <p style="font-size: 12px; color: #666;">
          This is an automated message from VUTAX. 
          <a href="{{unsubscribe_url}}">Unsubscribe</a>
        </p>
      </div>
    `;
  }
}
