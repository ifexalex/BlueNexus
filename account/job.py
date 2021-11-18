from .models import User



def Credit_balanace_reset():
    default_credit_balanace = 20000
    users = User.objects.all()
    
    for user in users:
        if user.credit_balance < default_credit_balanace:
            billing_amount = default_credit_balanace - user.credit_balance
            
           # bill_card (billing_amount)
           
            users.update(
                credit_balance = default_credit_balanace
            )
            
            print(f" Billing {user.first_name} NGN{billing_amount}")
        
            
            
            