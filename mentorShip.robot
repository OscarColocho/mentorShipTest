*** Settings ***
Library           RequestsLibrary
Library           OperatingSystem

*** Variables ***
${BASE_URL}       https://jsonplaceholder.typicode.com
${RESOURCE_PATH}  /posts

*** Test Cases ***

Get All Posts
    [Documentation]    Test to fetch all posts from the API.
    ${response}=    GET    ${BASE_URL}${RESOURCE_PATH}
    Should Be Equal As Integers    ${response.status_code}    200
    Log    ${response.json()}

Create A New Post
    [Documentation]    Test to create a new post in the API.
    ${data}=    Create Dictionary    title=Robot Test    body=This is a test post.    userId=1
    ${response}=    POST    ${BASE_URL}${RESOURCE_PATH}    json=${data}
    Should Be Equal As Integers    ${response.status_code}    201
    ${response_data}=    Evaluate    dict(${response.json()})    modules=json
    Log    Created Post: ${response_data}


Update A Post
    [Documentation]    Test to update an existing post in the API.
    ${data}=    Create Dictionary    id=1    title=Updated Title    body=Updated body text.    userId=1
    ${response}=    PUT    ${BASE_URL}${RESOURCE_PATH}/1    json=${data}
    Should Be Equal As Integers    ${response.status_code}    200
    ${response_data}=    Evaluate    dict(${response.json()})    modules=json
    Log    Updated Post: ${response_data}

Delete A Post
    [Documentation]    Test to delete a post from the API.
    ${response}=    DELETE    ${BASE_URL}${RESOURCE_PATH}/1
    Should Be Equal As Integers    ${response.status_code}    200
    Log    Post deleted successfully.