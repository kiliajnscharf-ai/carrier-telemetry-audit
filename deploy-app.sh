#!/usr/bin/env bash
set -euo pipefail

# ==================================================================
# ENVIRONMENT VARIABLES & CONFIGURATION
# ==================================================================
PROJECT_ID="gen-lang-client-0388537721"
ZONE="us-central1-a"
VM_NAME="test-vm"
MACHINE_TYPE="e2-micro"

# Replace <BILLING_ACCOUNT_ID> with your 18-character billing account ID
# Format: 012345-6789AB-CDEF01
BILLING_ACCOUNT_ID="<BILLING_ACCOUNT_ID>"
BUDGET_NAME="commercial-app-budget"
BUDGET_AMOUNT="100USD"

echo "=================================================="
echo "Starting deployment checks for Project: ${PROJECT_ID}"
echo "================================------------------"

# Ensure correct project context is selected
gcloud config set project "${PROJECT_ID}"

# ------------------------------------------------------------------
# STEP 1: Enable All Required APIs Explicitly
# ------------------------------------------------------------------
echo "Step 1: Enabling prerequisite APIs explicitly..."
gcloud services enable \
    serviceusage.googleapis.com \
    compute.googleapis.com \
    billingbudgets.googleapis.com

# ------------------------------------------------------------------
# STEP 2: Deploy Test VM Instance
# ------------------------------------------------------------------
echo "Step 2: Deploying virtual machine '${VM_NAME}' in zone '${ZONE}'..."
gcloud compute instances create "${VM_NAME}" \
    --zone="${ZONE}" \
    --machine-type="${MACHINE_TYPE}" \
    --image-family="debian-12" \
    --image-project="debian-cloud" \
    --restart-on-failure \
    --scopes="https://www.googleapis.com/auth/cloud-platform"

# ------------------------------------------------------------------
# STEP 3: Configure Billing Alerts & Budget
# ------------------------------------------------------------------
if [ "${BILLING_ACCOUNT_ID}" == "<BILLING_ACCOUNT_ID>" ] || [ -z "${BILLING_ACCOUNT_ID}" ]; then
    echo "Warning: No Billing Account ID provided. Skipping Step 3 (Budget creation)."
    echo "Please edit 'deploy-app.sh' and replace '<BILLING_ACCOUNT_ID>' to configure alerts."
else
    echo "Step 3: Provisioning budget alert '${BUDGET_NAME}'..."
    gcloud billing budgets create \
        --billing-account="${BILLING_ACCOUNT_ID}" \
        --display-name="${BUDGET_NAME}" \
        --budget-amount="${BUDGET_AMOUNT}" \
        --threshold-rule=percent=0.50 \
        --threshold-rule=percent=0.90 \
        --filter-projects="projects/${PROJECT_ID}"
fi

echo "================================------------------"
echo "Setup successfully completed!"
echo "================================------------------"
