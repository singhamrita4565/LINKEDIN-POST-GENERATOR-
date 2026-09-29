# 💼 LinkedIn Post Generator

An AI-powered LinkedIn Post Generator that creates, reviews, and improves LinkedIn posts using an iterative AI workflow.

Instead of generating a post only once, this project uses a **Writer Agent** and a **Reviewer Agent**. The Writer creates the LinkedIn post, while the Reviewer checks the generated content against predefined criteria. If the post is rejected, the reviewer's feedback is passed back to the Writer, which generates an improved version.

The Writer can also use **Tavily Web Search** when the topic requires recent information, current trends, or up-to-date facts.

The complete workflow is managed using **LangGraph**, while **Streamlit** provides a simple and interactive user interface.

---

## ✨ Features

- Generate LinkedIn posts from a user-provided topic
- AI-based review of generated posts
- Iterative improvement using reviewer feedback
- Web search using Tavily when current information is required
- Strong opening hook
- One clear and valuable takeaway
- Short and readable paragraphs
- Around 150–200 words
- Professional but human tone
- Ends with a question or call-to-action
- No hashtags
- Maximum of 3 writing attempts
- Simple and interactive Streamlit UI

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **LangGraph** | Workflow orchestration, state management, routing, and iterative loop |
| **LangChain** | LLM and tool integration |
| **Groq** | LLM inference |
| **Tavily** | Web search for current information |
| **Streamlit** | Web-based user interface |
| **python-dotenv** | Loading API keys from environment variables |

### Models Used

**Writer Model**
```text
qwen/qwen3.8-27b
```

**Reviewer Model**
```text
openai/gpt-oss-120b
```

---

## 🔄 How It Works

The application follows a **Generate → Review → Improve** workflow.

```text
User enters a topic
        ↓
    Writer Agent
        ↓
  Tool required?
     /       \
   Yes       No
    ↓         ↓
 Tavily     Generate
 Search      Draft
    ↓         ↓
   Writer ←───┘
      ↓
 Extract Draft
      ↓
 Reviewer Agent
      ↓
   Approved?
    /     \
  Yes      No
   ↓        ↓
 END     Feedback
            ↓
          Writer
            ↓
      Improved Draft
```

If the Writer needs current information, it can request a Tavily search. After the search results are returned, the Writer uses them to create the LinkedIn post.

Once the draft is ready, it is passed to the Reviewer.

If the Reviewer rejects the post, the feedback is stored in the LangGraph state and sent back to the Writer for another attempt.

The process continues until the post is approved or the maximum of 3 attempts is reached.

---

## 🧠 AI Workflow

### Writer Agent

The Writer is responsible for creating or improving the LinkedIn post.

It follows rules such as:

- Start with a strong hook
- Focus on one clear takeaway
- Use short paragraphs
- Keep the post around 150–200 words
- Maintain a professional but natural tone
- End with a question or call-to-action
- Avoid hashtags

The Writer is also connected to the Tavily search tool and can request web search when current information is needed.

### Reviewer Agent

The Reviewer evaluates the generated post using predefined criteria.

It checks:

1. Strong hook in the first line
2. One clear and valuable takeaway
3. Easy-to-read paragraph structure
4. Roughly 150–200 words
5. Engaging question or CTA at the end
6. Professional but human tone
7. No hashtags

The Reviewer returns a result in the following format:

```text
VERDICT: APPROVED
FEEDBACK: The post meets the required criteria.
```

or:

```text
VERDICT: REJECTED
FEEDBACK: The opening needs a stronger hook and the main takeaway should be clearer.
```

---

## 🔁 Iterative Improvement

One of the main ideas of this project is that the first generated response does not always have to be the final response.

For example:

```text
Draft 1
   ↓
Reviewer
   ↓
Rejected
   ↓
Reviewer Feedback
   ↓
Writer
   ↓
Draft 2
   ↓
Reviewer
   ↓
Approved
   ↓
Final Post
```

This makes the project different from a simple one-step LLM application.

A normal content generator might work like:

```text
Topic → LLM → Post
```

This project follows:

```text
Topic → Writer → Reviewer → Feedback → Writer → Final Post
```

---

## 🌐 Tavily Web Search

Tavily is integrated into the application as a search tool.

The Writer can decide when web search is useful.

For example, a topic such as:

```text
Latest trends in Generative AI
```

may require recent information.

The workflow can then become:

```text
Writer
   ↓
Requests Web Search
   ↓
Tavily
   ↓
Search Results
   ↓
Writer
   ↓
LinkedIn Draft
```

This allows the Writer to use fresh information when required.

---

## 🧩 LangGraph Workflow

The project uses LangGraph to connect different parts of the AI workflow.

### Main Nodes

**Writer**

Generates or rewrites the LinkedIn post.

**Tools**

Executes the Tavily search requested by the Writer.

**Extract Draft**

Takes the Writer's final response and stores it as the current draft.

**Reviewer**

Evaluates the draft and returns a verdict and feedback.

### Conditional Routing

The graph decides where to go next depending on the current state.

For example:

```text
Writer
   ↓
Tool call?
 ├── YES → Tools → Writer
 └── NO  → Extract Draft
```

After review:

```text
Reviewer
   ↓
Approved?
 ├── YES → END
 ├── Attempts >= 3 → END
 └── NO → Writer
```

---

## 📊 State Management

The workflow uses a shared state to pass information between different nodes.

The state contains:

```python
class State(TypedDict):
    topic: str
    messages: Annotated[list, add_messages]
    draft: str
    review_feedback: str
    is_approved: bool
    attempt: int
```

### State Fields

**`topic`**

Stores the topic provided by the user.

**`messages`**

Stores the conversation and tool-call history. This is important when the Writer needs to use the result returned by Tavily.

**`draft`**

Stores the current LinkedIn post.

**`review_feedback`**

Stores the feedback generated by the Reviewer.

**`is_approved`**

Stores whether the current draft is approved.

**`attempt`**

Keeps track of the number of writing attempts.

---

## 🖥️ Streamlit UI

The project includes a simple Streamlit interface so the user does not need to interact with the LangGraph workflow directly.

The UI provides:

- Topic input box
- Generate LinkedIn Post button
- Loading indicator
- Final LinkedIn post
- Reviewer verdict
- Number of attempts
- Reviewer feedback when applicable

The application is started using:

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
linkdinpost/
│
├── app.py
├── iterative.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

### `app.py`

Contains the Streamlit user interface.

It handles user input, creates the initial state, invokes the LangGraph workflow, and displays the final result.

### `iterative.py`

Contains the main AI workflow, including:

- LLM configuration
- Tavily search tool
- LangGraph state
- Writer node
- Tool node
- Draft extraction
- Reviewer node
- Conditional routing
- Iterative feedback loop
- Graph compilation

### `requirements.txt`

Contains the Python dependencies required by the application.

### `.env`

Stores API keys locally.

This file should not be uploaded to GitHub.

### `.gitignore`

Prevents local files such as `.venv`, `.env`, cache files, and editor settings from being committed.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd linkdinpost
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

For PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, your terminal should show:

```text
(.venv)
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Create the `.env` File

Create a file named:

```text
.env
```

Add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keep your API keys private and never commit them to GitHub.

---

## ▶️ Run the Application

Make sure the virtual environment is activated.

Then run:

```powershell
streamlit run app.py
```

You can also use:

```powershell
python -m streamlit run app.py
```

The application will open in your browser.

---

## 🖥️ Using the Application

Enter a topic such as:

```text
The impact of AI on software developers
```

Then click:

```text
Generate LinkedIn Post
```

The application will:

1. Send the topic to the Writer
2. Use Tavily if current information is needed
3. Generate a LinkedIn post
4. Send the draft to the Reviewer
5. Improve the post if it is rejected
6. Stop when the post is approved or 3 attempts are completed

The UI displays the final LinkedIn post, reviewer verdict, number of attempts, and feedback when applicable.

---

## 🧪 Example

### Input

```text
The impact of AI on software developers
```

### Workflow

```text
Writer
   ↓
Draft
   ↓
Reviewer
   ↓
REJECTED
   ↓
Reviewer Feedback
   ↓
Writer
   ↓
Improved Draft
   ↓
Reviewer
   ↓
APPROVED
```

### Final Output

```text
Verdict: APPROVED
Attempts: 2

Final LinkedIn Post:
[Generated LinkedIn post]
```

---

## 🎯 Why I Built This Project

I built this project to understand how iterative AI workflows work with LangGraph.

My goal was to move beyond a simple:

```text
Input → LLM → Output
```

approach and build a workflow where different AI components have different responsibilities.

The Writer focuses on generating the content, the Reviewer focuses on evaluating it, Tavily provides web search when needed, and LangGraph connects everything into a controlled workflow.

This project helped me understand how AI agents, tools, state management, conditional routing, and feedback loops can work together in a practical application.

---

## 📚 What I Learned

Through this project, I worked with:

- LangGraph StateGraph
- Nodes and edges
- Conditional edges
- Tool calling
- ToolNode
- Shared state
- LLM-based reviewing
- Iterative AI workflows
- Feedback loops
- Groq model integration
- Tavily web search
- Streamlit
- Environment variables
- Python virtual environments

The main concept I learned from this project is how multiple AI components can work together as a workflow instead of treating an LLM as a single function call.

---

## 🔐 Security

API keys are stored in environment variables instead of being written directly into the source code.

Example:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

The `.env` file should remain local and should be included in `.gitignore`.

Never upload real API keys to GitHub.

---

## 🚧 Current Limitations

The current version is intentionally simple.

- No database for storing previous posts
- No user authentication
- No permanent post history
- No direct LinkedIn publishing
- Reviewer criteria are predefined
- Maximum of 3 writing attempts
- Requires external API keys for Groq and Tavily

---

## 🔮 Future Improvements

Some improvements I would like to add in future versions:

- Different writing styles such as professional, storytelling, educational, and technical
- Tone selection
- Copy-to-clipboard functionality
- Post history
- Download generated posts
- Display every draft and review iteration
- More control over post length
- LinkedIn API integration
- Persistent storage for generated posts

---

## ⭐ Project Highlights

```text
✔ AI LinkedIn Post Generation
✔ AI-based Review
✔ Iterative Improvement
✔ Tavily Web Search
✔ LangGraph Workflow
✔ Conditional Routing
✔ Tool Calling
✔ Streamlit UI
✔ Feedback Loop
✔ Maximum 3 Attempts
```

---

## 👩‍💻 Author

**Amrita Singh**

Built as a hands-on project to learn and experiment with:

**Python | LangGraph | LangChain | Groq | Tavily | Streamlit**

---

## 📌 Core Idea

```text
Generate → Review → Improve → Repeat → Final Post
```

The project demonstrates how a simple AI content-generation task can be turned into a structured workflow with tool usage, evaluation, and iterative improvement.