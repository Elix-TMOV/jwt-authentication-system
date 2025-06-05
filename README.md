To run the front end 

1. npm install
2. npm run dev

To run the backend
1. create a virtual environment
2. pip install requirements.txt
3. uvicorn app.main:app --reload

There are heaps of improvents that can be build on top of this, I think the underlying system
In itself is a good starting points

A major concern for this implementation is that I am using the local storage of the browser to store the jwt token, but a much better way would be to store the jwt in httponly cookies
I used local storage cause it is easier to examine and explain 
