Chat UI Application
===================

This is a simple chat UI application built with React and `@chatscope/chat-ui-kit-react` library.

Prerequisites
-------------

-   Node.js (>=14.x)
-   npm (>=6.x)

Installation
------------

1.  Clone the repository:

```bash
git clone <repository-url>
```

1.  Navigate to the project directory:

```bash 
cd ui
```

1.  Install dependencies:

```bash
npm install
```

Running the Application
-----------------------

1.  Start the development server:

```bash
npm run dev
```

1.  Open your browser and navigate to:

```bash
http://localhost:3000/
```

File Upload
-----------

To upload a file, click on the attachment button and select a file from your system. A message will be displayed in the chat once the file is uploaded successfully.

Environment Variables
---------------------

Ensure you have a `.env` file in your project root with the following variables:

```env
VITE_REACT_APP_API_BASE_URL=<Your_API_Base_URL>
```