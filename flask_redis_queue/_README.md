# how to configure Redis 
https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04


# Start rq workers in the current directory 
rq worker 

# start flask 
python main.py 

# enqueue job with a json post 
http://reloadwa:5000/enqueue
JSON POST 

{
    "hello" : "world"
}

will return a job_id = b4278f22-e11b-4ef2-bf7e-8bec0ec0e238 (example) 

# check status 
http://reloadwa:5000/check_status?job_id=b4278f22-e11b-4ef2-bf7e-8bec0ec0e238

# get results 
http://reloadwa:5000/get_result?job_id=3e06c82e-db95-44c4-9f26-b866e6a4a38d

