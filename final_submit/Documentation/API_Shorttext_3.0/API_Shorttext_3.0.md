## API Documentation
### Keyword Endpoint :  `/prediction`
#### Type : `POST`


| Input Parameter  | Type | Constraints           |
|------------------|------|-----------------------|
| Text             | str  | No                    |
| Model            | str  | No                    |


![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.001.png)



* **Curl command**

    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.002.png)	



* **Return** 

    Returns output as JSON object with timestamp
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.003.png)

* **Error Codes**

    **500 - Prediction Module Error :** when error occurs inside the module

    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.004.png)

    **404 - Invalid model name**
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.006.png)

### Hashtag Endpoint :  `/prediction`
#### Type : `POST`

| Input Parameter  | Type | Constraints           |
|------------------|------|-----------------------|
| Text             | str  | No                    |
| Model            | str  | No                    |

![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.007.png)

* **Curl command**

    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.008.png)	

* **Return** 

    Returns output as JSON object with timestamp and token usage info. 
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.009.png)

* **Error Codes**

    **500 - Prediction Module Error :** when error occurs inside the module
    
    **![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.004.png)**

    **503 - Maintenance/Outage in OPENAI server**
    ![img.png](img.png)
    **401 – API Key is Invalid, Expired or Revoked**

    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.005.png)	
  
    **429 - Rate limit reached** - When maximum api calls per minute reached

  **404 - Invalid model name**
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.010.png)

### Topic Endpoint :  `/prediction`
#### Type : `POST`

| Input Parameter  | Type | Constraints           |
|------------------|------|-----------------------|
| Text             | str  | No                    |
| Model            | str  | No                    |

![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.011.png)

* **Curl command**

    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.012.png)

* **Return** 

    Returns output as JSON object with timestamp
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.013.png)

* **Error Codes**

    **500 - Prediction Module Error :** when error occurs inside the module
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.004.png)

    **404 - Invalid model name**
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.014.png)

### Zeroshot Endpoint :  `/prediction`
#### Type : `POST`

| Input Parameter   | Type | Constraints           |
|-------------------|------|-----------------------|
| Text              | str  | No                    |
| Labels (Optional) | list | Min 2 - Max 20 items  |
| Model             | str  | No                    |

![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.015.png)

* **Curl command**	

    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.016.png)

* **Return** 
    
    Returns output as JSON object with timestamp
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.017.png)	

* **Error Codes**
    
    **500 - Prediction Module Error :** when error occurs inside the  module
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.004.png)
    
    **404 - Invalid model name**
    
    ![](Aspose.Words.9bd4d685-bdc6-4707-99dd-3c42a4028a6a.018.png)
    


**::: END :::**
