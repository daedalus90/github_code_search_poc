import urllib.request, json, time, csv

def GetNextLinkFromHeader(linkHeader):
    print(linkHeader)
    headerParts = linkHeader.split(",")
    result = None
    for part in headerParts:
        if('rel="next"' in part):
            startIndex = part.index("<") + 1
            endIndex = part.index(">;")
            result = part[startIndex:endIndex]
    return result

def GetCodeSearchItemsResponse(searchUri):
    print("Pulling from: " + searchUri)
    req = urllib.request.Request(searchUri)
    req.add_header("Authorization", "token ***YOUR PAT TOKEN***")
    result = urllib.request.urlopen(req)
    time.sleep(10)
    return result

githubCodeSearchUri = "https://api.github.com/search/code"
#AzureWebJobsDashboard
searchTerm =  input("String to search for: ")
print(searchTerm)

reqUrl =  githubCodeSearchUri+"?q="+searchTerm
responseItems = []
loopCount = 0
while(reqUrl is not None):
    response = GetCodeSearchItemsResponse(reqUrl)
    rateLimitRemaining = response.getheader("X-RateLimit-Remaining")
    totalItems = response.getheader("X-RateLimit-Remaining")
    print("Remaining rate limit: " + rateLimitRemaining)
    linkHeader = response.getheader("Link")
    reqUrl = GetNextLinkFromHeader(linkHeader)
    responseString = response.read()
    responseObject = json.loads(responseString)
    responseItems = responseItems + responseObject["items"]
    loopCount = loopCount + 1
    print("Total items: " + str(responseObject["total_count"]) + " Items Processed: " + str(len(responseItems)))
    if(loopCount >= 1000):
        print("Max loop count reached")
        reqUrl = None

# name of csv file  
filename = "search_result_output.csv"
    
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(["owner_name","owner_page","owner_type","repo_full_name","code_page"])  
        
    # writing the data rows  
    for item in responseItems:
        csvwriter.writerow([item["repository"]["owner"]["login"], item["repository"]["owner"]["html_url"], item["repository"]["owner"]["type"], item["repository"]["full_name"], item["html_url"]]) 