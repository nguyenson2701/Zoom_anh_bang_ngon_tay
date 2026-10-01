#!/usr/bin/env bash
# Script cau hinh san quy tac bao ve nhanh main tren GitHub.
# Thay vi bam tung o trong Settings -> Branches, chay script nay 1 lan la xong.
#
# DIEU KIEN TRUOC KHI CHAY:
#   1. Da cai GitHub CLI (gh): https://cli.github.com
#   2. Da dang nhap:  gh auth login
#   3. Da tao repo tren GitHub va push code len nhanh main it nhat 1 lan
#      (repo trong hoan toan thi khong the bat branch protection)
#   4. Ban phai la chu repo (owner) hoac co quyen admin
#
# CACH CHAY:
#   cd vao thu muc repo da clone ve may, roi chay:
#   bash scripts/setup_branch_protection.sh

set -e

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Dang cau hinh branch protection cho repo: $REPO"

gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "repos/$REPO/branches/main/protection" \
  -f "required_status_checks[strict]=true" \
  -f "required_status_checks[contexts][]=check-python" \
  -F "enforce_admins=true" \
  -f "required_pull_request_reviews[required_approving_review_count]=1" \
  -F "restrictions="

echo "Da bat xong. Kiem tra lai tai: https://github.com/$REPO/settings/branches"
echo "Quy tac da bat: bat buoc Pull Request, bat buoc check CI (check-python) pass, bat buoc it nhat 1 nguoi approve, ap dung ca cho admin."
