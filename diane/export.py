"""Export functionality for diane records."""

import json
import csv
from pathlib import Path
from typing import List
from datetime import datetime

from .record import Record


class Exporter:
    """Handles exporting records to various formats."""

    @staticmethod
    def to_json(records: List[Record], pretty: bool = True) -> str:
        """Export records to JSON format.

        Args:
            records: List of records to export
            pretty: Whether to pretty-print JSON

        Returns:
            JSON string
        """
        data = []
        for record in records:
            data.append({
                'timestamp': record.timestamp.isoformat(),
                'content': record.content,
                'tags': record.tags,
                'sources': record.sources,
                'audio_file': record.audio_file,
            })

        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def to_csv(records: List[Record]) -> str:
        """Export records to CSV format.

        Args:
            records: List of records to export

        Returns:
            CSV string
        """
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(['timestamp', 'content', 'tags', 'sources'])

        # Rows
        for record in records:
            writer.writerow([
                record.timestamp.isoformat(),
                record.content,
                ','.join(record.tags) if record.tags else '',
                ','.join(record.sources) if record.sources else '',
            ])

        return output.getvalue()

    @staticmethod
    def to_html(records: List[Record], title: str = "diane, Records") -> str:
        """Export records to HTML format.

        Args:
            records: List of records to export
            title: Page title

        Returns:
            HTML string
        """
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'    <title>{title}</title>',
            '    <style>',
            '        body {',
            '            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
            '            max-width: 800px;',
            '            margin: 0 auto;',
            '            padding: 2rem;',
            '            background: #f5f5f5;',
            '        }',
            '        .record {',
            '            background: white;',
            '            padding: 1.5rem;',
            '            margin-bottom: 1rem;',
            '            border-radius: 8px;',
            '            box-shadow: 0 1px 3px rgba(0,0,0,0.1);',
            '        }',
            '        .timestamp {',
            '            color: #666;',
            '            font-size: 0.9rem;',
            '            margin-bottom: 0.5rem;',
            '        }',
            '        .tags {',
            '            display: inline-block;',
            '            margin-left: 1rem;',
            '        }',
            '        .tag {',
            '            display: inline-block;',
            '            background: #e3f2fd;',
            '            color: #1976d2;',
            '            padding: 0.2rem 0.6rem;',
            '            border-radius: 12px;',
            '            font-size: 0.85rem;',
            '            margin-right: 0.3rem;',
            '        }',
            '        .content {',
            '            line-height: 1.6;',
            '            white-space: pre-wrap;',
            '        }',
            '        h1 {',
            '            color: #333;',
            '            border-bottom: 2px solid #1976d2;',
            '            padding-bottom: 0.5rem;',
            '        }',
            '    </style>',
            '</head>',
            '<body>',
            f'    <h1>{title}</h1>',
        ]

        for record in records:
            timestamp_str = record.timestamp.strftime('%Y-%m-%d %H:%M:%S')

            tags_html = ''
            if record.tags:
                tags_html = '<span class="tags">'
                for tag in record.tags:
                    tags_html += f'<span class="tag">{tag}</span>'
                tags_html += '</span>'

            html_parts.extend([
                '    <div class="record">',
                '        <div class="timestamp">',
                f'            📅 {timestamp_str}',
                f'            {tags_html}',
                '        </div>',
                '        <div class="content">',
                f'            {record.content}',
                '        </div>',
                '    </div>',
            ])

        html_parts.extend([
            '</body>',
            '</html>',
        ])

        return '\n'.join(html_parts)

    @staticmethod
    def to_markdown(records: List[Record]) -> str:
        """Export records to a single Markdown document.

        Args:
            records: List of records to export

        Returns:
            Markdown string
        """
        md_parts = [
            '# diane, Records Export',
            '',
            f'Exported: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '',
            '---',
            '',
        ]

        for record in records:
            timestamp_str = record.timestamp.strftime('%Y-%m-%d %H:%M:%S')

            md_parts.append(f'## {timestamp_str}')
            md_parts.append('')

            if record.tags:
                tags_str = ' '.join(f'`{tag}`' for tag in record.tags)
                md_parts.append(f'**Tags:** {tags_str}')
                md_parts.append('')

            md_parts.append(record.content)
            md_parts.append('')
            md_parts.append('---')
            md_parts.append('')

        return '\n'.join(md_parts)

    @staticmethod
    def save_export(content: str, filepath: Path) -> None:
        """Save exported content to file.

        Args:
            content: Content to save
            filepath: Path to save to
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
