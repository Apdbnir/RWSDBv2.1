"""
SQL Syntax Highlighter for PyQt6
Provides syntax highlighting for SQL keywords in QTextEdit widgets
"""
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt6.QtCore import QRegularExpression, Qt


class SqlSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Define formats for different SQL elements
        self.keyword_format = self._create_format("#FFA500", QFont.Weight.Bold)  # Orange for keywords (sections)
        self.function_format = self._create_format("#800080", QFont.Weight.Bold)  # Purple for functions
        self.aggregate_function_format = self._create_format("#006400", QFont.Weight.Bold)  # Dark green for aggregate functions
        self.string_format = self._create_format("#FFFFFF", QFont.Weight.Normal)  # White for strings
        self.number_format = self._create_format("#00FF00", QFont.Weight.Normal)  # Green for numbers
        self.comment_format = self._create_format("#808080", QFont.Weight.Normal, True)  # Gray for comments
        self.operator_format = self._create_format("#FF0000", QFont.Weight.Bold)  # Red for operators
        self.subquery_format = self._create_format("#FFFF00", QFont.Weight.Bold)  # Yellow for subqueries
        self.table_column_format = self._create_format("#008080", QFont.Weight.Normal)  # Teal for table/column names

        # Define aggregate functions separately
        self.aggregate_functions = [
            'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'STDDEV', 'VARIANCE',
            'GROUP_CONCAT', 'STRING_AGG', 'ARRAY_AGG'
        ]

        # Define SQL keywords
        self.keywords = [
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER',
            'TABLE', 'INDEX', 'VIEW', 'TRIGGER', 'PROCEDURE', 'FUNCTION',
            'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'CROSS', 'ON',
            'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT', 'OFFSET', 'UNION', 'ALL',
            'AND', 'OR', 'NOT', 'IN', 'EXISTS', 'BETWEEN', 'LIKE', 'IS', 'NULL',
            'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'UNIQUE', 'CHECK', 'DEFAULT',
            'INT', 'INTEGER', 'VARCHAR', 'TEXT', 'DATE', 'DATETIME', 'TIMESTAMP',
            'BOOLEAN', 'FLOAT', 'DOUBLE', 'DECIMAL', 'SERIAL', 'BIGINT',
            'INTO', 'VALUES', 'SET', 'AS', 'DISTINCT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
            'ASC', 'DESC', 'TRUE', 'FALSE', 'COMMIT', 'ROLLBACK', 'BEGIN',
            'DATABASE', 'SCHEMA', 'IF', 'EXCEPT', 'INTERSECT', 'MINUS'
        ]

        # Define SQL functions (excluding aggregate functions which are handled separately)
        self.functions = [
            'UPPER', 'LOWER', 'LENGTH', 'SUBSTRING', 'CONCAT', 'TRIM',
            'ROUND', 'CEIL', 'FLOOR', 'ABS', 'POWER', 'SQRT', 'MOD',
            'NOW', 'DATE', 'TIME', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND',
            'COALESCE', 'IFNULL', 'NULLIF', 'CAST', 'CONVERT',
            'EXTRACT', 'STRFTIME', 'JULIANDAY'
        ]

        # Define SQL operators
        self.operators = [
            '=', '!=', '<>', '<', '>', '<=', '>=', '+', '-', '*', '/', '%',
            '||', '&', '|', '^', '~', '<<', '>>', '!'
        ]

    def _create_format(self, color, weight=QFont.Weight.Normal, italic=False):
        """Create a QTextCharFormat with specified properties"""
        format_ = QTextCharFormat()
        format_.setForeground(QColor(color))
        format_.setFontWeight(weight)
        if italic:
            format_.setFontItalic(True)
        return format_

    def highlightBlock(self, text):
        """Apply syntax highlighting to a block of text"""
        # First pass: highlight subqueries (content between parentheses that contains SELECT-like keywords)
        # Start with simpler approach - find basic parentheses groups and check for SQL keywords inside
        start = 0
        while start < len(text):
            # Find opening parenthesis
            open_pos = text.find('(', start)
            if open_pos == -1:
                break  # No more opening parentheses

            # Find matching closing parenthesis
            paren_count = 1
            pos = open_pos + 1
            while pos < len(text) and paren_count > 0:
                if text[pos] == '(':
                    paren_count += 1
                elif text[pos] == ')':
                    paren_count -= 1
                pos += 1

            if paren_count == 0:
                # We found a matching pair
                close_pos = pos - 1
                subquery_text = text[open_pos + 1:close_pos]

                # Check if this contains SQL keywords indicating it's a subquery
                if any(keyword.lower() in subquery_text.lower() for keyword in ['select', 'from', 'where', 'group', 'order', 'having']):
                    # Highlight the entire parentheses group as a subquery
                    self.setFormat(open_pos, close_pos - open_pos + 1, self.subquery_format)

            start = open_pos + 1

        # Highlight keywords
        for keyword in self.keywords:
            pattern = QRegularExpression(r'\b' + keyword + r'\b',
                                       QRegularExpression.PatternOption.CaseInsensitiveOption)
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

        # Highlight aggregate functions first (before regular functions)
        for function in self.aggregate_functions:
            pattern = QRegularExpression(r'\b' + function + r'\b\(\s*',
                                       QRegularExpression.PatternOption.CaseInsensitiveOption)
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                # Highlight the function name part (before the parenthesis)
                func_name_end = match.capturedStart() + len(function)
                self.setFormat(match.capturedStart(), func_name_end - match.capturedStart(), self.aggregate_function_format)

        # Highlight regular functions
        for function in self.functions:
            pattern = QRegularExpression(r'\b' + function + r'\b\(\s*',
                                       QRegularExpression.PatternOption.CaseInsensitiveOption)
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                # Highlight the function name part (before the parenthesis)
                func_name_end = match.capturedStart() + len(function)
                self.setFormat(match.capturedStart(), func_name_end - match.capturedStart(), self.function_format)

        # Highlight strings (single and double quotes)
        string_pattern = QRegularExpression(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"")
        match_iterator = string_pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

        # Highlight numbers (including decimal points)
        number_pattern = QRegularExpression(r'\b\d+\.?\d*\b')
        match_iterator = number_pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.number_format)

        # Highlight SQL comments (-- and /* */)
        single_line_comment = QRegularExpression(r'--.*')
        multi_line_comment = QRegularExpression(r'/\*.*?\*/')

        match_iterator = single_line_comment.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)

        match_iterator = multi_line_comment.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)

        # Highlight operators
        for operator in self.operators:
            # For operators like =, !=, <>, etc., we don't use word boundaries since they're not words
            escaped_operator = QRegularExpression.escape(operator)
            pattern = QRegularExpression(escaped_operator)
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.operator_format)