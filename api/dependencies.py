from analytics.logger import AnalyticsLogger, analytics_logger


def get_analytics_logger() -> AnalyticsLogger:
    """Dependency for analytics logger"""
    return analytics_logger
