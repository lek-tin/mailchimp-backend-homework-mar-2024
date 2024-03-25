## What is this
Solution to the [Mailchimp Backend Takehome Project](https://gist.github.com/mc-interviews/305a6d7d8c4ba31d4e4323e574135bf9)

## What does it do
Converts markdown text to html

## How to run app as a web service
```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
python app-web.py
```
Now you can `post` to `http://127.0.0.1:5000/convert-markdown-to-html` for use it.
### Option 1: use a API client, such as Postman
![Web Service Demo](/images/web_service_demo.png)
### Option 2: curl
```bash
curl -X POST http://127.0.0.1:5000/convert-markdown-to-html \
   -H 'Content-Type: application/json' \
   -d '{"markdown_text":"Hello!\nThis is sample markdown for the [Mailchimp](https://www.mailchimp.com) homework assignment."}'
```

## How to run app as a cli tool
```bash
# slow mode: outputs the result on console
./app-cli.py --markdown_file_path="test_files/large_markdown_file.md"
# optimized mode: multi-threaded, outputs the result under /html_result folder
./app-cli.py --markdown_file_path="test_files/large_markdown_file.md" --optimized
# turn on debug_mode to see logs
./app-cli.py --markdown_file_path="test_files/large_markdown_file.md" --debug_mode
./app-cli.py --markdown_file_path="test_files/large_markdown_file.md" --optimized --debug_mode
```

## How to test
### Unit Tests
```bash
python test.py
```

## Clean-up
After you finish using the web service, stop the virtual environment using the following command
```bash
deactivate
```

## Self-evaluation
* Functionality
    * Does the code do what it should?
        * ✅ see in `test.py`
    * Does it handle edge cases?
        * ✅ see in `test.py`
* Code quality
    * Is the code readable & maintainable?
        * ✅ see comments
    * Is there reasonable test coverage?
        * ✅ see in `test.py`
* Performance
    * Does the code balance reasonably fast execution with readability?
    * Can the implementation handle large inputs gracefully?
        * ✅ Yes, there is a optimized version that processes the markdown input with multi threads, and partial files are generated

