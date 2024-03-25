from markdown_to_html import convert_markdown_to_html
import unittest

class TestMarkdownToHtmlConversion(unittest.TestCase):
  def test_empty_input(self):
    # blank line should be ignored
    actual_output = convert_markdown_to_html('   ')
    expected_output = ''
    self.assertEqual(actual_output, expected_output)
    # consecutive newlines => empty output
    actual_output = convert_markdown_to_html('\n\n\n')
    expected_output = ''
    self.assertEqual(actual_output, expected_output)

  def test_standalon_paragraphs(self):
    actual_output = convert_markdown_to_html('123\n456\n789\n')
    expected_output = '<p>123</p>\n<p>456</p>\n<p>789</p>'
    self.assertEqual(actual_output, expected_output)

  def test_standalon_headings(self):
    actual_output = convert_markdown_to_html('# heading 1\n## heading 2\n### heading 3\n#### heading 4\n##### heading 5\n###### heading 6\n####### heading 7')
    # Only Heading 1 - 6 are expected
    expected_output = '<h1>heading 1</h1>\n<h2>heading 2</h2>\n<h3>heading 3</h3>\n<h4>heading 4</h4>\n<h5>heading 5</h5>\n<h6>heading 6</h6>\n<p>####### heading 7</p>'
    self.assertEqual(actual_output, expected_output)

  def test_nested_headings(self):
    actual_output = convert_markdown_to_html('# heading 1 ### nested text\n## heading 2')
    # Nested headings is not supproted
    expected_output = '<h1>heading 1 ### nested text</h1>\n<h2>heading 2</h2>'
    self.assertEqual(actual_output, expected_output)

  def test_embeded_hyperlinks(self):
    # hyperlink embedded in heading tag
    actual_output = convert_markdown_to_html('## This is sample markdown for the [Mailchimp](https://www.mailchimp.com) homework assignment.')
    expected_output = '<h2>This is sample markdown for the <a href="https://www.mailchimp.com">Mailchimp</a> homework assignment.</h2>'
    self.assertEqual(actual_output, expected_output)
    # hyperlink embedded in paragraph tag
    actual_output = convert_markdown_to_html('Hello!\nThis is sample markdown for the [Mailchimp](https://www.mailchimp.com) homework assignment.')
    expected_output = '<p>Hello!</p>\n<p>This is sample markdown for the <a href="https://www.mailchimp.com">Mailchimp</a> homework assignment.</p>'
    self.assertEqual(actual_output, expected_output)
    ## hyperlinks embedded in both heading and paragraph tags
    actual_output = convert_markdown_to_html("# Header one\nHello there\nHow are you?\nWhat's going on?\n## Another Header\nThis is a paragraph [with an inline link](http://google.com). Neat, eh?\n## This is a header [with a link](http://yahoo.com)")
    expected_output = '<h1>Header one</h1>\n<p>Hello there</p>\n<p>How are you?</p>\n<p>What\'s going on?</p>\n<h2>Another Header</h2>\n<p>This is a paragraph <a href="http://google.com">with an inline link</a>. Neat, eh?</p>\n<h2>This is a header <a href="http://yahoo.com">with a link</a></h2>'
    self.assertEqual(actual_output, expected_output)

if __name__ == "__main__":
  unittest.main()