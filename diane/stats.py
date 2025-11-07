"""Statistics and analytics for diane records."""

from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, List

from .record import Record


class Statistics:
    """Generate statistics about records."""

    def __init__(self, records: List[Record]):
        self.records = records

    def total_count(self) -> int:
        """Get total number of records."""
        return len(self.records)


    def records_by_date(self) -> Dict[str, int]:
        """Get count of records per day."""
        date_counter = Counter()

        for record in self.records:
            date_str = record.timestamp.strftime('%Y-%m-%d')
            date_counter[date_str] += 1

        return dict(sorted(date_counter.items()))

    def recent_activity(self, days: int = 7) -> Dict[str, int]:
        """Get record counts for recent days.

        Args:
            days: Number of days to include

        Returns:
            Dictionary mapping date strings to counts
        """
        cutoff = datetime.now() - timedelta(days=days)
        date_counter = Counter()

        for record in self.records:
            if record.timestamp >= cutoff:
                date_str = record.timestamp.strftime('%Y-%m-%d')
                date_counter[date_str] += 1

        return dict(sorted(date_counter.items()))

    def word_count(self) -> int:
        """Get total word count across all records."""
        total = 0
        for record in self.records:
            total += len(record.content.split())
        return total

    def average_words_per_record(self) -> float:
        """Get average words per record."""
        if not self.records:
            return 0.0

        total_words = self.word_count()
        return total_words / len(self.records)

    def busiest_day(self) -> tuple:
        """Get the day with most records.

        Returns:
            Tuple of (date_string, count)
        """
        by_date = self.records_by_date()
        if not by_date:
            return None, 0

        busiest = max(by_date.items(), key=lambda x: x[1])
        return busiest

    def summary(self) -> Dict:
        """Get a comprehensive statistics summary."""
        busiest_date, busiest_count = self.busiest_day()

        return {
            'total_records': self.total_count(),
            'total_words': self.word_count(),
            'avg_words_per_record': round(self.average_words_per_record(), 1),
            'busiest_day': busiest_date,
            'busiest_day_count': busiest_count,
        }
