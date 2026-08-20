# CG Cloud Data Model — API Reference

Complete list of CG Cloud objects organized by functional area with their API names.

## Table of Contents
1. [Customer Master](#customer-master)
2. [Organization Unit](#organization-unit)
3. [Customer Sets & Segmentation](#customer-sets--segmentation)
4. [Asset](#asset)
5. [Product Master](#product-master)
6. [Product Assortment](#product-assortment)
7. [User / Substitution](#user--substitution)
8. [Advanced Promotions](#advanced-promotions)
9. [Visit Planning](#visit-planning)
10. [Activities: Planning and Execution](#activities-planning-and-execution)
11. [Advanced Order](#advanced-order)
12. [Penny Perfect Pricing](#penny-perfect-pricing)
13. [Customer Task](#customer-task)
14. [Inventory Control](#inventory-control)

---

## Customer Master

| Object | API Name |
|--------|----------|
| Account (Customer) | `Account` |
| Trade Org Hierarchy | `cgcloud__Account_Trade_Org_Hierarchy__c` |
| Customer Extension | `cgcloud__Account_Extension__c` |
| Contact | `Contact` |
| Customer Relationship | `cgcloud__Account_Relationship__c` |
| POS (Point of Sale) | `cgcloud__POS__c` |
| Listing Classification | `cgcloud__Listing_Classification__c` |
| Account Receivable | `cgcloud__Account_Receivable__c` |
| Customer Template | `cgcloud__Account_Template__c` |
| Operating Hours | `OperatingHours` |

## Organization Unit

| Object | API Name |
|--------|----------|
| Org Unit | `cgcloud__Org_Unit__c` |
| Org Unit Hierarchy | `cgcloud__Org_Unit_Hierarchy__c` |
| Org Unit User | `cgcloud__Org_Unit_User__c` |
| Customer Org Unit | `cgcloud__Account_Org_Unit__c` |
| Customer Manager | `cgcloud__Account_Manager__c` |
| User | `User` |
| Sales Organization | `cgcloud__Sales_Organization__c` |
| Flatten Org Unit Hierarchy | `cgcloud__Flatten_Org_Unit_Hierarchy__c` |

## Customer Sets & Segmentation

| Object | API Name |
|--------|----------|
| Customer Set | `cgcloud__Account_Set__c` |
| Customer Set Customer | `cgcloud__Account_Set_Account__c` |
| Segmentation Rule | `cgcloud__Segmentation_Rule__c` |
| Promotion | `Promotion` |
| Pricing Condition | `cgcloud__CP_Pricing_Condition__c` |
| Activity | `Activity` |
| Activity Customer Set | `cgcloud__Job_Definition_List_Account_Set__c` |

## Asset

| Object | API Name |
|--------|----------|
| Asset Template | `cgcloud__Asset_Template__c` |
| Asset | `Asset` |
| Asset Audit | `cgcloud__Asset_Audit__c` |
| Customer Task | `cgcloud__Account_Task__c` |

## Product Master

| Object | API Name |
|--------|----------|
| Product Template | `cgcloud__Product_Template__c` |
| Product | `Product2` |
| Product Hierarchy | `cgcloud__Product_Hierarchy__c` |
| Warehouse | `cgcloud__Warehouse__c` |
| Warehouse Product | `cgcloud__Warehouse_Product__c` |
| Product Part (BOM) | `cgcloud__Product_Part__c` |
| Unit of Measure | `cgcloud__Unit_of_Measure__c` |
| Conditions (Product Prices) | `cgcloud__CP_Pricing_Condition__c` |

## Product Assortment

| Object | API Name |
|--------|----------|
| Product Assortment Template | `cgcloud__Product_Assortment_Template__c` |
| Product Assortment | `AssortmentProduct` |
| Listing Modules | `cgcloud__Listing_Module__c` |
| Product Listing Modules | `cgcloud__Product_Listing_Module__c` |
| Product Assortment Store | `cgcloud__Product_Assortment_Store__c` |

## User / Substitution

| Object | API Name |
|--------|----------|
| User | `User` |
| Sales Organization User | `cgcloud__Sales_Organization_User__c` |
| Substitution | `cgcloud__Substitution__c` |
| Customer Substitution | `cgcloud__Customer_Substitution__c` |

## Advanced Promotions

| Object | API Name |
|--------|----------|
| Tactic Template | `cgcloud__Tactic_Template__c` |
| Tactic | `cgcloud__Tactic__c` |
| Tactic Product | `cgcloud__Tactic_Product__c` |
| Promotion Template | `cgcloud__Promotion_Template__c` |
| Customer Set | `cgcloud__Account_Set__c` |
| Promotion Attachment | `cgcloud__Promotion_Attachment__c` |
| Promotion Sales Folder | `cgcloud__Promotion_Sales_Folder__c` |

## Visit Planning

| Object | API Name |
|--------|----------|
| Visit Template | `cgcloud__Visit_Template__c` |
| Visit | `Visit` |
| Event | `Event` |
| Trip List | `cgcloud__Trip_List__c` |
| Trip List Customer | `cgcloud__Trip_List_Account__c` |
| Job Lists | `cgcloud__Job_List__c` |
| Customer Visit Settings | `cgcloud__Account_Visit_Setting__c` |
| Sales Org User | `cgcloud__Sales_Organization_User__c` |

## Activities: Planning and Execution

| Object | API Name |
|--------|----------|
| Data Type | `cgcloud__Data_Type__c` |
| Data Type Option | `cgcloud__Data_Type_Option__c` |
| Job Template | `cgcloud__Job_Template__c` |
| Job Definition Template | `cgcloud__Job_Definition_Template__c` |
| Template Question | `cgcloud__Job_DL_Template_Def_Template__c` |
| Activity Template | `cgcloud__Job_Definition_List_Template__c` |
| Assigned Question | `cgcloud__Job_DL_Job_Definition_Template__c` |
| Activity | `cgcloud__Job_Definition_List__c` |
| Field Sales Activity | `cgcloud__Field_Sales_Activity__c` |
| Activity Product | `cgcloud__Job_Definition_List_Product__c` |
| Activity Customer | `cgcloud__Job_Definition_List_Account__c` |
| Activity Customer Set | `cgcloud__Job_Definition_List_Account_Set__c` |
| Visit Job | `cgcloud__Visit_Job__c` |
| POS Template | `cgcloud__POS_Template__c` |
| POS | `cgcloud__POS__c` |
| Job List | `cgcloud__Job_List__c` |

## Advanced Order

| Object | API Name |
|--------|----------|
| Order Template | `cgcloud__Order_Template__c` |
| Advanced Order | `cgcloud__Order__c` |
| Advanced Order Item | `cgcloud__Order_Item__c` |
| Unit of Measure | `cgcloud__Unit_of_Measure__c` |
| Signature | `cgcloud__Signature__c` |

## Penny Perfect Pricing

| Object | API Name |
|--------|----------|
| Pricing Condition Template | `cgcloud__CP_Pricing_Condition_Template__c` |
| Complex Pricing Condition | `cgcloud__CP_Pricing_Condition__c` |
| Calculation Schema Determination | `cgcloud__CP_Calculation_Schema_Determination__c` |
| Calculation Schema | `cgcloud__CP_Calculation_Schema__c` |
| Calculation Schema Steps | `cgcloud__CP_Calculation_Schema_Step__c` |
| Search Strategy | `cgcloud__CP_Search_Strategy__c` |
| Search Strategy Steps | `cgcloud__CP_Search_Strategy_Step__c` |
| Key Type | `cgcloud__CP_Key_Type__c` |
| Key Attribute | `cgcloud__CP_Key_Attribute__c` |

## Customer Task

| Object | API Name |
|--------|----------|
| Customer Task Template | `cgcloud__Account_Task_Template__c` |
| Customer Task | `cgcloud__Account_Task__c` |

## Inventory Control

| Object | API Name |
|--------|----------|
| Inventory Control Template | `cgcloud__Inventory_Control_Template__c` |
| Inventory | `cgcloud__Inventory__c` |
| Inventory Transaction Template | `cgcloud__Inventory_Transaction_Template__c` |
| Inventory Transaction | `cgcloud__Inventory_Transaction__c` |
| Order Item Inventory Transaction | `cgcloud__Order_Item_Inventory_Transaction__c` |
| Order Payment Inventory Transaction | `cgcloud__Order_Payment_Inventory_Transaction__c` |
| Tour | `cgcloud__Tour__c` |
| Vehicle | `cgcloud__Vehicle__c` |

---

## Naming Convention Notes

- All custom CG Cloud objects use the `cgcloud__` namespace prefix
- Standard Salesforce objects used: `Account`, `Contact`, `Product2`, `Asset`, `Visit`, `Event`, `User`, `OperatingHours`
- The `Promotion` object is the standard Salesforce Promotion object (not custom)
- "Customer" in CG Cloud terminology maps to the standard `Account` object
- "Activity" in CG Cloud maps to `cgcloud__Job_Definition_List__c` (not the standard Activity object)
- "Visit Job" contains survey/question answers captured during visit execution
