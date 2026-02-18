@echo off
echo Organizing documentation files...
echo.

REM Create archive directory
if not exist "docs\archive" mkdir "docs\archive"

REM Move old documentation files
move /Y "BACKEND_EXPLANATION_UPGRADE.md" "docs\archive\" 2>nul
move /Y "BACKEND_INTEGRATION_COMPLETE.md" "docs\archive\" 2>nul
move /Y "BACKEND_NOT_RUNNING.md" "docs\archive\" 2>nul
move /Y "BACKEND_RULE_SYSTEM_CREATED.md" "docs\archive\" 2>nul
move /Y "BACKEND_UPGRADE_COMPLETE.md" "docs\archive\" 2>nul
move /Y "COMPLETE_IMPLEMENTATION_GUIDE.md" "docs\archive\" 2>nul
move /Y "COMPLETE_SYSTEM_UPGRADE.md" "docs\archive\" 2>nul
move /Y "COMPLETION_SUMMARY.md" "docs\archive\" 2>nul
move /Y "DOWNLOAD_FEATURE.md" "docs\archive\" 2>nul
move /Y "FINAL_DELIVERY.md" "docs\archive\" 2>nul
move /Y "FINAL_STRUCTURE.md" "docs\archive\" 2>nul
move /Y "FINAL_UPGRADE_STATUS.md" "docs\archive\" 2>nul
move /Y "FIRST_TIME_SETUP.md" "docs\archive\" 2>nul
move /Y "FIX_APPLIED.md" "docs\archive\" 2>nul
move /Y "IMPLEMENTATION_STATUS.md" "docs\archive\" 2>nul
move /Y "INDIA_CONTEXT.md" "docs\archive\" 2>nul
move /Y "INDIA_LOCALIZATION_SUMMARY.md" "docs\archive\" 2>nul
move /Y "JUDGE_UPGRADES_COMPLETE.md" "docs\archive\" 2>nul
move /Y "JUDICIAL_SAFETY_COMPLETE.md" "docs\archive\" 2>nul
move /Y "KEY_FACTORS_DATA_DISPLAY.md" "docs\archive\" 2>nul
move /Y "LOCALIZATION_UPDATE.md" "docs\archive\" 2>nul
move /Y "PROFESSIONAL_IMPROVEMENTS.md" "docs\archive\" 2>nul
move /Y "PROFILE_DATA_SAMPLES_ADDED.md" "docs\archive\" 2>nul
move /Y "PROFILE_PAGE_INTEGRATION.md" "docs\archive\" 2>nul
move /Y "PROFILE_PAGE_JUDICIAL_UPGRADES.md" "docs\archive\" 2>nul
move /Y "PROFILE_PAGE_USER_GUIDE.md" "docs\archive\" 2>nul
move /Y "PROJECT_STRUCTURE.md" "docs\archive\" 2>nul
move /Y "QUICK_FIX_ACCOUNT_CREATION.md" "docs\archive\" 2>nul
move /Y "QUICK_FIX_SIGNIN.md" "docs\archive\" 2>nul
move /Y "REGULATORY_SUBMISSION.md" "docs\archive\" 2>nul
move /Y "REGULATORY_UPGRADE_COMPLETE.md" "docs\archive\" 2>nul
move /Y "RULE_BASED_TRANSFORMATION.md" "docs\archive\" 2>nul
move /Y "RULE_COMPLETION_FIXES_COMPLETE.md" "docs\archive\" 2>nul
move /Y "SIMPLE_START_GUIDE.md" "docs\archive\" 2>nul
move /Y "TESTING_COMPLETE.md" "docs\archive\" 2>nul
move /Y "TESTING_GUIDE.md" "docs\archive\" 2>nul
move /Y "UI_COPY_UPGRADES.md" "docs\archive\" 2>nul
move /Y "UI_FORMATTING_IMPROVEMENTS.md" "docs\archive\" 2>nul
move /Y "UI_UPGRADE_SPECIFICATIONS.md" "docs\archive\" 2>nul
move /Y "UI_UPGRADES_IMPLEMENTED.md" "docs\archive\" 2>nul
move /Y "UPGRADE_CHECKLIST.md" "docs\archive\" 2>nul
move /Y "UPGRADE_COMPLETE_SUMMARY.md" "docs\archive\" 2>nul
move /Y "UPGRADE_STATUS_CHECK.md" "docs\archive\" 2>nul
move /Y "UPGRADES_COMPLETED.md" "docs\archive\" 2>nul
move /Y "WHATS_NEW.md" "docs\archive\" 2>nul
move /Y "WORK_COMPLETED.txt" "docs\archive\" 2>nul

REM Move important docs to proper locations
move /Y "DEPLOYMENT_CHECKLIST.md" "docs\" 2>nul
move /Y "JUDGE_PRESENTATION.md" "docs\" 2>nul
move /Y "QUICK_QA_GUIDE.md" "docs\" 2>nul
move /Y "QUICKSTART.md" "docs\" 2>nul
move /Y "RULE_COMPLETION_FRAMEWORK_FINAL.md" "docs\" 2>nul
move /Y "SYSTEM_FLOWCHART.md" "docs\" 2>nul

echo.
echo Documentation organized!
echo - Old files moved to: docs\archive\
echo - Important files moved to: docs\
echo.
pause
