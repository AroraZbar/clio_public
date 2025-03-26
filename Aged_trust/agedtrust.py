import streamlit as st
import pandas as pd
import numpy as np
import webbrowser
import threading
import time

def process_trust_data(df, client_col, account_col, balance_col, date_col):
    df.columns = df.columns.str.strip()  # remove extra whitespace
    df[balance_col] = df[balance_col].str.replace(r'[^\d\.-]', '', regex=True)
    df[balance_col] = pd.to_numeric(df[balance_col], errors='coerce')
    
    today = pd.Timestamp.now().date()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df['Days Since Last Activity'] = (pd.Timestamp(today) - df[date_col]).dt.days
    
    df = df.sort_values(date_col)
    df[date_col] = df[date_col].dt.strftime('%Y-%m-%d')
    df[date_col] = df[date_col].fillna('N/A')
    df['Days Since Last Activity'] = pd.to_numeric(df['Days Since Last Activity'], errors='coerce').astype("Int64")
    
    # Standardize field names for later use
    df['Client'] = df[client_col]
    df['Account'] = df[account_col]
    df['Client Balance'] = df[balance_col]
    df['Last Activity Date'] = df[date_col]
    
    # Omit rows with $0 balance
    df = df[df['Client Balance'] != 0]
    
    return df

def main():
    import sys
    
    # Updated title block:
    st.title("Trust Account Activity Analyzer")
    st.image("https://arorazbar.com/wp-content/uploads/2020/12/Arora_Zbar.svg", width=150)
    st.markdown("Powered By Arora Zbar LLP")
    
    # Add instructional text
    instructions_text = """
    ### Instructions:
    1. First, get the "Trust Listing Report" from Clio.
    2. Upload the file.
    3. Ensure the columns are correctly mapped to the required fields.
    4. Review the aged trust listing, with the number of days calculated and sortable by last activity.
    5. Download the processed data as a CSV.   
    """
    st.markdown(instructions_text)
    
    # Add a clickable link for Clio
    st.markdown(
        '[Open Clio Trust Listing](https://app.clio.com/nc/#/reports/trust_listing)',
        unsafe_allow_html=True
    )
    
    st.write("Upload your Clio 'Trust Listing Report' CSV to analyze days since last activity")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read CSV specifying the required columns to avoid extra empty fields
            df = pd.read_csv(uploaded_file, usecols=["Client", "Account", "Last Activity Date", "Client Balance"])
            
            # Let the user select the column mapping for every required field
            client_col = st.selectbox(
                "Select column for Client",
                options=df.columns.tolist(),
                index=df.columns.tolist().index("Client") if "Client" in df.columns.tolist() else 0
            )
            account_col = st.selectbox(
                "Select column for Account",
                options=df.columns.tolist(),
                index=df.columns.tolist().index("Account") if "Account" in df.columns.tolist() else 0
            )
            balance_col = st.selectbox(
                "Select column for Client Balance",
                options=df.columns.tolist(),
                index=df.columns.tolist().index("Client Balance") if "Client Balance" in df.columns.tolist() else 0
            )
            date_col = st.selectbox(
                "Select column for Last Activity Date",
                options=df.columns.tolist(),
                index=df.columns.tolist().index("Last Activity Date") if "Last Activity Date" in df.columns.tolist() else 0
            )
            
            df = process_trust_data(df, client_col, account_col, balance_col, date_col)
            
            st.subheader("Trust Account Summary")
            total_accounts = len(df)
            total_balance = df['Client Balance'].sum()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Accounts", total_accounts)
            with col2:
                st.metric("Total Balance", f"${total_balance:,.2f}")
            
            # Calculate grouped summary
            account_summary = df.groupby('Account', as_index=False)['Client Balance'].sum()
            account_summary['Client Balance'] = account_summary['Client Balance'].apply(lambda x: f"${x:,.2f}")
            
            # New option: choose display mode
            display_mode = st.radio("Select Display Mode", ["Single Listing", "Split Listings"])
            
            if display_mode == "Split Listings":
                st.subheader("Trust Account Listing - Detailed")
                st.dataframe(df)
                st.subheader("Trust Account Listing - Grouped by Account")
                # For each account, display individual clients and their balances.
                for account in df["Account"].unique():
                    st.markdown(f"**Account: {account}**")
                    account_clients = df[df["Account"] == account][["Client", "Client Balance"]]
                    st.dataframe(account_clients)
            else:
                st.subheader("Trust Account Listing (Detailed)")
                st.dataframe(df)
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Processed Data as CSV",
                data=csv,
                file_name="trust_account_analysis.csv",
                mime="text/csv",
            )
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    elif page == "Payment Tracking":
        st.subheader("Payment Tracking System")
        tab1, tab2, tab3 = st.tabs(["Record Payment", "Payment History", "Balance Summary"])
        
        # ...existing code for tab1 and tab2...
        
        with tab3:
            st.write("### Balance Summary")
            
            completed_payments = [p for p in load_payments() if p["status"] == "Completed"]
            
            if completed_payments:
                # ...existing code to compute current payment balances...
                all_payment_parties = set()
                for p in completed_payments:
                    all_payment_parties.add(p["from"])
                    all_payment_parties.add(p["to"])
                
                balances = []
                for party in sorted(all_payment_parties):
                    paid_out = sum(p["amount"] for p in completed_payments if p["from"] == party)
                    received = sum(p["amount"] for p in completed_payments if p["to"] == party)
                    net_balance_party = received - paid_out
                    balances.append({
                        "Party": party,
                        "Paid Out": paid_out,
                        "Received": received,
                        "Net Balance": net_balance_party
                    })
                
                balance_df = pd.DataFrame(balances)
                
                st.write("#### Current Payment Balances")
                st.dataframe(
                    balance_df.style.format({
                        "Paid Out": format_dollars,
                        "Received": format_dollars,
                        "Net Balance": format_dollars
                    }),
                    use_container_width=True
                )
                
                # Reconciliation Section: Use corrected net invoice from Attorney Fee Reconciliation Summary
                st.write("#### Reconciliation with Calculated Fees")
                st.write("Using a corrected invoice value (-net_invoice) to adjust payments.")
                
                recon_list = []
                for att in df_net[attorney_col].unique():
                    # Compute net invoice as before (total due - total owed)
                    fees_due = df_net[df_net[attorney_col] == att]
                    total_due = fees_due["Fee"].sum()
                    fees_owe = df_net[(df_net[user_col] == att) & (df_net[attorney_col] != att)]
                    total_owe = fees_owe["Fee"].sum()
                    net_invoice = total_due - total_owe
                    # Flip the sign so that a negative net_invoice becomes a positive corrected value
                    corrected_invoice = -net_invoice
                    # Deduct payments (both made and received reduce the outstanding amount)
                    final_net_balance = corrected_invoice - sum(p["amount"] for p in completed_payments if p["from"] == att) - sum(p["amount"] for p in completed_payments if p["to"] == att)
                    
                    recon_list.append({
                        "Attorney": att,
                        "Corrected Invoice": corrected_invoice,
                        "Payments Made (From Attorney)": sum(p["amount"] for p in completed_payments if p["from"] == att),
                        "Payments Received (To Attorney)": sum(p["amount"] for p in completed_payments if p["to"] == att),
                        "Final Reconciled Balance": final_net_balance
                    })
                
                if recon_list:
                    df_recon = pd.DataFrame(recon_list)
                    st.dataframe(
                        df_recon.style.format({
                            "Corrected Invoice": format_dollars,
                            "Payments Made (From Attorney)": format_dollars,
                            "Payments Received (To Attorney)": format_dollars,
                            "Final Reconciled Balance": format_dollars
                        }),
                        use_container_width=True
                    )
                else:
                    st.info("No reconciliation data available.")
            else:
                st.info("No completed payments to display balance summary.")

if __name__ == "__main__":
    main()
