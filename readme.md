Presents various sources of current most active Reuters stocks, python demo.
Implements selenium headless Chrome driver as a windows cmd server.
Only one source file, 'mostactivestocks.py', no css files due to webdriver_manager.chrome restriction.
To run windows cmd server, unzip the exe\dist.zip package, created by 'python setup.py py2exe', see setup.py for the included files.
Run 'mostactivestocks.exe' at a cmd prompt, starts the server listening on localhost:8080, use -host and -port switches to override.
Client browser to 'http://localhost:8080/mostactivestocks', read the notes for the how to.
The top line is a series of links which generate the presented tables, sourced for the 'ReutersMostActive' website, added value is the per market symbol link to its 'Yahoo Finance' website, browser back arrow.
SYMBOL field queries any stock to "Yahoo Finance",
Investing.com link provides more realtme updates, news etc.
