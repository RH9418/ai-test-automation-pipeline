# AI Test Automation Pipeline 🚀

An end-to-end AI-powered factory that transforms brittle, raw Playwright Codegen recordings into robust, human-in-the-loop Pytest suites, complete with comprehensive Markdown User Acceptance Testing (UAT) documentation and styled Excel reports.

Powered by **Playwright**, **LangGraph**, **CrewAI**, and **Azure OpenAI (GPT-4o)**.

---

## 📂 Architecture & Directory Structure

The pipeline moves scripts sequentially through dedicated directories to ensure zero data loss and perfect isolation:

* `Codegen_Logs/` ➔ Raw Playwright recordings.
* `Enhanced_Logs/` ➔ Scripts injected with Spotlight screenshots and manual fallbacks.
* `Enhancement_Reports/` ➔ Text reports detailing which actions were successfully wrapped vs. missed by the regex parser.
* `Test_Screenshots/` ➔ UI snapshots captured chronologically during enhanced script execution.
* `Execution_Reports/` ➔ Text reports tracking how many actions succeeded vs. required manual human intervention during a run.
* `Annotated_Logs/` ➔ Raw scripts injected with precise, AI-generated business logic comments.
* `Generated_Documentation/` ➔ Markdown UAT tables documenting the exact user flows.
* `UAT_Excel_Reports/` ➔ Formatted, client-ready Excel versions of the UAT tables.
* `Generated_Scripts/` ➔ The final, modular, state-aware Pytest automation suite.

---

## 🛠️ Prerequisites & Setup

### 1. Install Dependencies

Ensure you are using Python 3.10+ and have activated your virtual environment.

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Environment Variables

Create a `.env` file in the root of your project and configure your Azure OpenAI credentials and rate-limiting rules:

```env
AZURE_API_KEY="your_api_key_here"
AZURE_ENDPOINT="https://your-resource.openai.azure.com/"
AZURE_API_VERSION="2024-06-01"
AZURE_DEPLOYMENT_NAME="gpt-4o"
PYTHONIOENCODING="UTF-8"
CREWAI_TELEMETRY_DISABLED="true"
OTEL_SDK_DISABLED="true"
RATE_LIMIT_DELAY=15
```

---

## ⚙️ Step-by-Step Workflow

### Step 1: Record the Raw Flow (Codegen)

Use Playwright's built-in codegen tool to record your user journey. Save the output directly into the `Codegen_Logs` directory.

*Note: Every click and action matters; do not worry about repetitive steps.*

```bash
playwright codegen "https://your-target-spa-url.com" -o Codegen_Logs/my_feature.py 
```

### Step 2: Enhance the Script

The enhancer script wraps raw Playwright actions in a `safe_action` paradigm. This injects Javascript "Spotlights" (red bounding boxes) to highlight elements and adds manual fallbacks if an action fails. It also generates an `Enhancement_Report`.

```bash
python enhance_playwright_scripts_with_report.py

# Or for a specific file: 
python enhance_playwright_scripts_with_report.py --files my_feature.py
```
**Output:** `Enhanced_Logs/my_feature.py` and `Enhancement_Reports/my_feature_Report.txt`

### Step 3: Execute the Enhanced Script (Capture Visual Context)

Run the newly enhanced script. This execution is crucial—it navigates the browser and saves annotated screenshots for every single UI action into isolated subdirectories. When the script finishes, it automatically saves an `Execution_Report`.

```bash
python Enhanced_Logs/my_feature.py
```
**Output:** Images populated in `Test_Screenshots/my_feature/` and a runtime report in `Execution_Reports/`

### Step 4: Generate AI Annotations

Using LangGraph (Planner-Worker architecture with an Overlap Sliding Window), the AI reads the raw code and the sequence of screenshots, chunks them semantically, and injects highly accurate business-logic comments into the script without hallucinating.

```bash
python generate_annotations.py

# Or for a specific file: 
python generate_annotations.py --files my_feature.py
```
**Output:** `Annotated_Logs/my_feature.py`

### Step 5: Generate Artifacts (Docs, Excel & Pytest)

Using CrewAI and Procedural Python Generation, the orchestrator processes the fully annotated script to generate downstream artifacts safely and quickly.

* **Phase 1 (CrewAI):** Generates a strict Markdown UAT table.
* **Phase 2 (Procedural):** Instantly generates a modular, robust Pytest script using regex mapping (0 LLM tokens, 0 dropped lines).
* **Phase 3 (Procedural):** Converts the Markdown UAT table into a perfectly styled Excel sheet.

```bash
python generate_artifacts_procedural.py

# Or for a specific file: 
python generate_artifacts_procedural.py --files my_feature.py
```
*Note: You can run specific phases using `--step 1`, `--step 2`, or `--step 3`.*

**Outputs:**
* `Generated_Documentation/My Feature_UAT.md`
* `Generated_Scripts/test_my_feature.py`
* `UAT_Excel_Reports/My Feature_UAT.xlsx`

### Step 6: Run the Final Automated Tests

Run your newly generated Pytest suite.

**CRITICAL:** You must run this with the `-s` flag. The `-s` flag prevents Pytest from capturing standard input/output, allowing the `safe_action` pauses and terminal prompts (Human-in-the-loop fallbacks) to function properly during dynamic SPA testing.

```bash
pytest Generated_Scripts/test_my_feature.py -v -s
```

---

## 🧠 Advanced Notes

* **Rate Limiting:** Because the pipeline relies heavily on the Azure OpenAI API, it chunks massive files and respects the `RATE_LIMIT_DELAY` defined in your `.env`. It also features incremental timeouts (adding 5s upon failure) to prevent 429 Token limit errors.
* **Human-In-The-Loop:** If the Pytest execution fails to find an element due to SPA rendering delays, the script will pause, alert you in the terminal, and wait for you to perform the action manually in the Chromium window before continuing.
* **Smart Caching:** Step 5 caches the semantic chunk boundaries to a local JSON file. If you need to regenerate the Pytests (Step 2) or the Excel file (Step 3), it executes instantly without wasting tokens on Azure.
* **Fixtures:** The generated Pytests rely on a `shared_page` fixture. Ensure you have a `conftest.py` file inside your `Generated_Scripts` directory that yields a Playwright page context.
