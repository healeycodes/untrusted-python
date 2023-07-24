"use client"
import { useEffect, useState } from "react";
import CodeEditor from '@uiw/react-textarea-code-editor';

const API = process.env.API

export default function Home() {
  const [code, setCode] = useState(`# hint: use cmd + enter to submit\nimport random\n\nprint(f"Hello, World!")\nprint(random.randint(0, 1000))`);
  const [loading, setLoading] = useState(false)
  const [output, setOutput] = useState(``);
  useEffect(() => {
    // Wake up API to avoid a cold start for `/api/exec`
    fetch(`${API}/api/ping`)
      .then(r => {
        if (r.status !== 200) {
          console.error(`/api/ping responded with non-200`, r.status, r.statusText)
        }
      })
      .catch(e => console.error(e))
  }, []);


  const exec = async () => {
    setLoading(true)
    try {
      const r = await fetch(`${API}/api/exec`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code })
      });
      if (r.status !== 200) {
        setOutput(`server responded with ${r.status}${r.statusText ? ": " + r.statusText : ""}`)
        return
      }
      const text = (await r.text()).trim()
      if (text === '') {
        setOutput("(sandbox didn't produce any stdout/stderr)")
      } else {
        setOutput(text)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // "Cmd" or "Ctrl" and "Enter"
    if ((e.metaKey || e.ctrlKey) && e.keyCode === 13) {
      exec()
      return false
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4 md:p-24">
      <form onSubmit={(e) => { e.preventDefault(); exec() }}>
        <div className="space-y-12">
          <div className="grid grid-cols-1 gap-x-8 gap-y-10 border-b border-gray-900/10 pb-12 md:grid-cols-3">
            <div>
              <h2 className="text-base font-semibold leading-7 text-gray-900">isolated-python</h2>
              <p className="mt-1 text-sm leading-6 text-gray-600">
                Run some untrusted Python code.
                <br/>
                Will open source this soon!
              </p>
            </div>

            <div className="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 md:col-span-2">
              <div className="col-span-full">
                <label htmlFor="code" className="block text-sm font-medium leading-6 text-gray-900">
                  Code
                </label>
                <div className="mt-2">
                  <CodeEditor
                    autoFocus
                    value={code}
                    language="py"
                    onChange={(evn) => setCode(evn.target.value)}
                    onKeyDown={handleKeyDown}
                    padding={15}
                    style={{
                      fontSize: 14,
                      // bg-slate-100
                      backgroundColor: "rgb(241 245 249)",
                      fontFamily: 'ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace',
                    }}
                  />
                </div>
                <p className="mt-3 text-sm leading-6 text-gray-600">The above code is passed to an <a className="text-sky-600" href="https://docs.python.org/3/library/functions.html#exec">exec</a> call on the server – stdout/stderr will be displayed below.</p>
              </div>

              <div className="col-span-full gap-x-6">
                <button
                  type="submit"
                  className={`float-right rounded-md bg-blue-500 px-3 py-2 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 ${loading ? 'bg-slate-400' : 'hover:bg-blue-600'}`}
                >
                  Submit
                </button>
              </div>

              <div className="col-span-full gap-x-6">
                {output !== '' && <pre
                  className="text-sm whitespace-pre-wrap break-words p-3 bg-slate-100"
                  // Use the comment color from the editor
                  style={{ color: '#6e7781', }}
                >
                  {output}
                </pre>}
              </div>
            </div>
          </div>
        </div>

      </form>
    </main>
  )
}
