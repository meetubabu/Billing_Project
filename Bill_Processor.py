import json
import time
import os
import Prod_Details
l_bills_path = "C:\\Users\\meetu\\learnings\\Assignments\\BILLING_PROJECT\\Bills"
outfile1="C:\\Users\\meetu\\learnings\\Assignments\\BILLING_PROJECT\\Processed_Bills"
errorfile="C:\\Users\\meetu\\learnings\\Assignments\\BILLING_PROJECT\\Error_Bills"

os.chdir(l_bills_path)

def read_json_file(file_path):
    new_file = open(file_path, "r")
    var_text = json.loads(new_file.read())
    new_file.close()
    bill_prod_detals=var_text["BillDetails"]
    
    #get the product details from data 
    prod_details_data={}
    for dict1 in Prod_Details.Product_details:
        prod_details_data[dict1["prod_id"]] = dict1["unit_price"]

    hasError = False

    #getlinetotal amd bill total
    Linetotal_list=[]
    billtotal=0
    for prodId in bill_prod_detals.keys():
        if prodId in prod_details_data.keys():
            linetotal= bill_prod_detals[prodId] * prod_details_data[prodId]
            billtotal=billtotal+linetotal
            Linetotal_list.append({"Product":prodId,"Qty":bill_prod_detals[prodId],"linetotal":linetotal})
        else:
            hasError = True
            break

    if hasError == False:
        #append bill details to line total list
        processed_bill={"LineItems":Linetotal_list,"BillID":var_text["BillID"],"BillDate":var_text["BillDate"],"StoreID":var_text["StoreID"],"BillTotal":billtotal}
        print(processed_bill)

        #write to processed file folder
        with open(f"{outfile1}\\{file}","w") as outfile:
            outfile.write(json.dumps(processed_bill))
    else:
        err_txt=json.dumps(var_text)
        with open(f"{errorfile}\\{file}","w") as errfile: #write to error folder
            errfile.write(err_txt)


# iterate through all file
for file in os.listdir():
    # Check whether file is in json format or not
    if file.endswith(".json"):
        file_path = f"{l_bills_path}\\{file}"

        # call read json file function
        read_json_file(file_path)
    
