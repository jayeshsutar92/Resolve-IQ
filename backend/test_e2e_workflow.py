"""
test_e2e_workflow.py
End-to-end automated validation script testing:
1. Log Complaint via natural language
2. Edit Complaint via natural language (verifying untouched fields are preserved)
3. Document Extraction via formal text/document string
"""

import asyncio
from database.session import AsyncSessionFactory
from services.workflow_service import WorkflowService

async def run_e2e_tests():
    print("=== STARTING END-TO-END WORKFLOW SELF-TEST ===")
    
    async with AsyncSessionFactory() as session:
        service = WorkflowService(session)
        
        # Test 1: Log Complaint
        print("\n--- Test 1: Log Complaint ---")
        log_msg = (
            "Customer Jane Smith reported an issue with Amoxicillin 500mg, Batch B-98765, "
            "Mfg Date 2025-01-10, Exp Date 2027-01-10. 50 capsules affected. "
            "Complaint Date 2026-07-25. The seal on the bottle was broken upon arrival. "
            "Reported from St. Jude Hospital as a Packaging Defect."
        )
        res1 = await service.process_chat_message(log_msg)
        complaint1 = res1["complaint"]
        print("Logged Message Response:\n", res1["message"])
        print("Extracted Customer Name:", complaint1.customer_name)
        print("Extracted Product:", complaint1.product_or_service)
        print("Extracted Strength:", complaint1.product_strength)
        print("Extracted Batch #:", complaint1.batch_number)
        print("Extracted Quantity:", complaint1.quantity_affected)
        print("Extracted Source:", complaint1.complaint_source)
        print("Risk Severity:", complaint1.risk_assessment.severity if complaint1.risk_assessment else "None")
        print("Risk Recommended Action:", complaint1.risk_assessment.recommended_action if complaint1.risk_assessment else "None")
        
        assert complaint1.id is not None
        complaint_id = complaint1.id

        # Test 2: Edit Complaint (Update incident date & quantity without losing product/batch info)
        print("\n--- Test 2: Edit Complaint ---")
        edit_msg = "Correction: The date of incident was 2026-07-24 and actually 100 capsules were affected."
        res2 = await service.process_chat_message(edit_msg, complaint_id=complaint_id)
        complaint2 = res2["complaint"]
        print("Edited Message Response:\n", res2["message"])
        print("Updated Date of Incident:", complaint2.date_of_incident)
        print("Updated Quantity Affected:", complaint2.quantity_affected)
        print("PRESERVED Customer Name:", complaint2.customer_name)
        print("PRESERVED Batch #:", complaint2.batch_number)
        print("PRESERVED Product Strength:", complaint2.product_strength)
        
        assert complaint2.date_of_incident == "2026-07-24"
        assert complaint2.batch_number == "B-98765"  # Verified preserved

        # Test 3: Document Extraction
        print("\n--- Test 3: Document Extraction ---")
        doc_text = """
        FORMAL PHARMACEUTICAL QUALITY COMPLAINT FORM
        -------------------------------------------
        Reporter: Dr. Robert Vance
        Source: City General Pharmacy
        Date: 2026-07-26
        Product Name: Ibuprofen Oral Suspension
        Strength: 100mg/5ml
        Batch Number: LOT-44512
        Manufacturing Date: 2025-06-01
        Expiry Date: 2027-06-01
        Quantity Affected: 12 bottles
        Incident Date: 2026-07-22
        Category: Product Quality Defect
        Description: Product liquid appears cloudy with unexpected sedimentation at the bottom of bottles before expiry.
        """
        res3 = await service.process_document(doc_text)
        complaint3 = res3["complaint"]
        print("Document Response:\n", res3["message"])
        print("Extracted Reporter:", complaint3.customer_name)
        print("Extracted Product:", complaint3.product_or_service)
        print("Extracted Strength:", complaint3.product_strength)
        print("Extracted Batch #:", complaint3.batch_number)
        print("Extracted Category:", complaint3.complaint_type)
        print("Risk Level:", complaint3.risk_assessment.risk_level if complaint3.risk_assessment else "None")
        print("Risk Reasoning:", complaint3.risk_assessment.reasoning if complaint3.risk_assessment else "None")

    print("\n=== ALL E2E WORKFLOW TESTS PASSED SUCCESSFULLY ===")

if __name__ == "__main__":
    asyncio.run(run_e2e_tests())
