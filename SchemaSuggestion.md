# Client side schema suggestion

To consume these AI services, sample client code in python language has been provided in respective folders. The designed AI services are well suited for short texts such as townhall posts.

You can call these services immediately as and when the new content (townhall post) arrives on the platform or you can run it as scheduled job.


For every posts, you may wan to save the following data in the database. These are just the guideline and not the exact suggestion:

```json
{
    "townhall_post_id": 2,
    "topic": {
            "value": ["topic1","topic2","topic3"],
            "model_name": "model1",
            "api_version":"v1",
            "time_stamp": <timestamp>,
        },
    "keyword": {
            "value": ["kw1","kw2","kw3"],
            "model_name": "model1",
            "api_version":"v1",
            "time_stamp": <timestamp>,
        },
    "hashtag": {
            "value": ["ht1","ht2","ht3"],
            "model_name": "model1",
            "api_version":"v1",
            "time_stamp": <timestamp>,
        },
}
```