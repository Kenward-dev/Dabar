"""This module contains utility functions for sending emails in the Taskly application."""

from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_welcome_email(to_email, username=None):
    """Send a welcome email to newly registered users."""
    subject = "Welcome to Taskly"
    if username:
        message = f"Hi {username}, \n\n Welcome to Taskly! \nYour account has been created successfully. \n\n You can now start organizing your tasks and boost your productivity. \n\n Happy task managing! \n\n Best regards,\n\n Taskly Team."
    else:
        message = "Thanks for registering!"
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False
        )
        logger.info(f"Welcome email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email}: {str(e)}")
        return False

def send_task_reminder_email(to_email, username, task_title, due_date=None):
    """Send a task reminder email to users."""
    subject = f"Reminder: {task_title}"
    
    if due_date:
        message = f"Hi {username},\n\nThis is a reminder about your task: '{task_title}' which is due on {due_date}.\n\nBest regards,\nTaskly Team"
    else:
        message = f"Hi {username},\n\nThis is a reminder about your task: '{task_title}'.\n\nBest regards,\nTaskly Team"
    
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False
        )
        logger.info(f"Task reminder email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send task reminder email to {to_email}: {str(e)}")
        return False

def send_password_reset_email(to_email, username, reset_link):
    """Send a password reset email to users."""
    subject = "Password Reset - Taskly"
    message = f"Hi {username},\n\nYou requested a password reset. Click the link below to reset your password:\n\n{reset_link}\n\nIf you didn't request this, please ignore this email.\n\nBest regards,\nTaskly Team"
    
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False
        )
        logger.info(f"Password reset email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send password reset email to {to_email}: {str(e)}")
        return False

def send_task_created_email(to_email, username, task_title, task_description=None, due_date=None):
    """Send a confirmation email when a new task is created."""
    subject = f"New Task Created: {task_title}"
    
    message = f"Hi {username},\n\n"
    message += f"Your new task '{task_title}' has been successfully created.\n\n"
    
    if task_description:
        message += f"Description: {task_description}\n\n"
    
    if due_date:
        message += f"Due Date: {due_date}\n\n"
    
    message += "You can view and manage your tasks on your Taskly dashboard.\n\n"
    message += "Best regards,\nTaskly Team"
    
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False
        )
        logger.info(f"Task created email sent successfully to {to_email} for task: {task_title}")
        return True
    except Exception as e:
        logger.error(f"Failed to send task created email to {to_email} for task {task_title}: {str(e)}")
        return False
