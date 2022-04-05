from http.server import BaseHTTPRequestHandler, HTTPServer
from mostactivestocks import MostActiveStocks

# ------------------------------------------------------------------------
#                       WebServer
# ------------------------------------------------------------------------

# http://localhost:8080/api/MostActiveStocks
# http://localhost:8080/api/mostactivestocks?market=nyse

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        MostActiveStocks.marketListInit()
        url = f'http://{MostActiveStocks.hostName}:{MostActiveStocks.serverPort}{self.path}'
        args = f'{url}'.split("=")
        market = args[1] if len(args) > 1 else ''
        homePath = f'{url}'
        marketUrl = ''
        for item in MostActiveStocks.marketList:
            if item[0].lower() == market.lower():
                marketName = item[0]
                marketUrl = item[1]
                break

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if marketUrl == '':
            self.wfile.write(MostActiveStocks.getHomeStr(homePath).encode("utf-8"))
        else :
            htmlTitle, tableData = MostActiveStocks.getJson(marketUrl, marketName)
            self.wfile.write(MostActiveStocks.getDataStr(htmlTitle, homePath, tableData).encode("utf-8"))

if __name__ == "__main__": 
    MostActiveStocks.configInit()
    webServer = HTTPServer((MostActiveStocks.hostName, MostActiveStocks.serverPort), WebServer)
    print(f'Server started {MostActiveStocks.hostName}:{MostActiveStocks.serverPort}')
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
