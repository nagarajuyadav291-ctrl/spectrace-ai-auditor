"""
Intelligent Alert System
Multi-channel notifications with smart routing
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from discord_webhook import DiscordWebhook, DiscordEmbed
from twilio.rest import Client as TwilioClient

class AlertManager:
    """Manage multi-channel alerts and notifications"""
    
    def __init__(self):
        # Email configuration
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL")
        
        # Slack configuration
        self.slack_token = os.getenv("SLACK_BOT_TOKEN")
        self.slack_channel = os.getenv("SLACK_CHANNEL", "#spectrace-alerts")
        self.slack_client = WebClient(token=self.slack_token) if self.slack_token else None
        
        # Discord configuration
        self.discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        
        # Twilio configuration
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from_number = os.getenv("TWILIO_FROM_NUMBER")
        self.twilio_client = TwilioClient(
            self.twilio_account_sid, 
            self.twilio_auth_token
        ) if self.twilio_account_sid else None
        
        # Alert rules
        self.alert_rules = {
            'critical': ['email', 'slack', 'discord', 'sms'],
            'high': ['email', 'slack', 'discord'],
            'medium': ['slack', 'discord'],
            'low': ['discord']
        }
    
    async def send_alert(self, alert_data: Dict):
        """
        Send alert through appropriate channels based on severity
        
        Args:
            alert_data: {
                'severity': 'critical|high|medium|low',
                'title': 'Alert title',
                'message': 'Alert message',
                'execution_id': 123,
                'risk_score': 0.85,
                'violations': [...],
                'recipients': ['email@example.com']
            }
        """
        severity = alert_data.get('severity', 'medium')
        channels = self.alert_rules.get(severity, ['discord'])
        
        # Send to each configured channel
        for channel in channels:
            try:
                if channel == 'email':
                    await self._send_email_alert(alert_data)
                elif channel == 'slack':
                    await self._send_slack_alert(alert_data)
                elif channel == 'discord':
                    await self._send_discord_alert(alert_data)
                elif channel == 'sms':
                    await self._send_sms_alert(alert_data)
            except Exception as e:
                print(f"Failed to send {channel} alert: {str(e)}")
    
    async def _send_email_alert(self, alert_data: Dict):
        """Send email alert"""
        if not self.smtp_username or not self.smtp_password:
            return
        
        recipients = alert_data.get('recipients', [])
        if not recipients:
            return
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[SpecTrace] {alert_data['title']}"
        msg['From'] = self.from_email
        msg['To'] = ', '.join(recipients)
        
        # HTML email body
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white;">
              <h1>🔍 SpecTrace Alert</h1>
            </div>
            <div style="padding: 20px;">
              <h2 style="color: #667eea;">{alert_data['title']}</h2>
              <p><strong>Severity:</strong> <span style="color: {'#ef4444' if alert_data['severity'] == 'critical' else '#f59e0b'};">{alert_data['severity'].upper()}</span></p>
              <p><strong>Execution ID:</strong> {alert_data.get('execution_id', 'N/A')}</p>
              <p><strong>Risk Score:</strong> {alert_data.get('risk_score', 0):.2f}</p>
              <hr>
              <p>{alert_data['message']}</p>
              
              {self._format_violations_html(alert_data.get('violations', []))}
              
              <hr>
              <p style="color: #6b7280; font-size: 12px;">
                Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
              </p>
            </div>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
    
    async def _send_slack_alert(self, alert_data: Dict):
        """Send Slack alert"""
        if not self.slack_client:
            return
        
        # Color based on severity
        color_map = {
            'critical': '#ef4444',
            'high': '#f59e0b',
            'medium': '#3b82f6',
            'low': '#10b981'
        }
        
        color = color_map.get(alert_data['severity'], '#6b7280')
        
        # Create Slack message
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🔍 {alert_data['title']}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Severity:*\n{alert_data['severity'].upper()}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Risk Score:*\n{alert_data.get('risk_score', 0):.2f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Execution ID:*\n{alert_data.get('execution_id', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{datetime.utcnow().strftime('%H:%M:%S UTC')}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": alert_data['message']
                }
            }
        ]
        
        # Add violations if present
        violations = alert_data.get('violations', [])
        if violations:
            violation_text = "\n".join([
                f"• *{v['rule_name']}* ({v['severity']}): {v['description']}"
                for v in violations[:5]
            ])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Violations:*\n{violation_text}"
                }
            })
        
        try:
            self.slack_client.chat_postMessage(
                channel=self.slack_channel,
                blocks=blocks,
                text=alert_data['title']
            )
        except SlackApiError as e:
            print(f"Slack API error: {e.response['error']}")
    
    async def _send_discord_alert(self, alert_data: Dict):
        """Send Discord alert"""
        if not self.discord_webhook_url:
            return
        
        webhook = DiscordWebhook(url=self.discord_webhook_url)
        
        # Color based on severity
        color_map = {
            'critical': 0xef4444,
            'high': 0xf59e0b,
            'medium': 0x3b82f6,
            'low': 0x10b981
        }
        
        embed = DiscordEmbed(
            title=f"🔍 {alert_data['title']}",
            description=alert_data['message'],
            color=color_map.get(alert_data['severity'], 0x6b7280)
        )
        
        embed.add_embed_field(
            name="Severity",
            value=alert_data['severity'].upper(),
            inline=True
        )
        embed.add_embed_field(
            name="Risk Score",
            value=f"{alert_data.get('risk_score', 0):.2f}",
            inline=True
        )
        embed.add_embed_field(
            name="Execution ID",
            value=str(alert_data.get('execution_id', 'N/A')),
            inline=True
        )
        
        # Add violations
        violations = alert_data.get('violations', [])
        if violations:
            violation_text = "\n".join([
                f"• **{v['rule_name']}** ({v['severity']})"
                for v in violations[:5]
            ])
            embed.add_embed_field(
                name="Violations",
                value=violation_text,
                inline=False
            )
        
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
    
    async def _send_sms_alert(self, alert_data: Dict):
        """Send SMS alert via Twilio"""
        if not self.twilio_client:
            return
        
        phone_numbers = alert_data.get('phone_numbers', [])
        if not phone_numbers:
            return
        
        message_body = (
            f"SpecTrace Alert\n"
            f"{alert_data['title']}\n"
            f"Severity: {alert_data['severity'].upper()}\n"
            f"Risk: {alert_data.get('risk_score', 0):.2f}\n"
            f"Execution: {alert_data.get('execution_id', 'N/A')}"
        )
        
        for phone in phone_numbers:
            try:
                self.twilio_client.messages.create(
                    body=message_body,
                    from_=self.twilio_from_number,
                    to=phone
                )
            except Exception as e:
                print(f"Failed to send SMS to {phone}: {str(e)}")
    
    def _format_violations_html(self, violations: List[Dict]) -> str:
        """Format violations for HTML email"""
        if not violations:
            return ""
        
        html = "<h3>Violations Detected:</h3><ul>"
        for v in violations[:5]:
            html += f"<li><strong>{v['rule_name']}</strong> ({v['severity']}): {v['description']}</li>"
        html += "</ul>"
        
        if len(violations) > 5:
            html += f"<p><em>...and {len(violations) - 5} more violations</em></p>"
        
        return html
    
    def configure_alert_rules(self, rules: Dict[str, List[str]]):
        """Configure custom alert routing rules"""
        self.alert_rules.update(rules)
