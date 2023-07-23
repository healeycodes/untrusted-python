"use client"
import { useState } from "react";

export default function Home() {
  const [code, setCode] = useState(`print("Hello, World!")`);
  const [output, setOutput] = useState(``);
  const exec = async () => {
    const r = await fetch('/api/exec', {
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
    setOutput(await r.text())
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <form onSubmit={(e) => { e.preventDefault(); exec() }}>
        <div className="space-y-12">
          <div className="grid grid-cols-1 gap-x-8 gap-y-10 border-b border-gray-900/10 pb-12 md:grid-cols-3">
            <div>
              <h2 className="text-base font-semibold leading-7 text-gray-900">isolated-python</h2>
              <p className="mt-1 text-sm leading-6 text-gray-600">
                This is an example of how to run untrusted Python code.
              </p>
            </div>

            <div className="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 md:col-span-2">
              <div className="col-span-full">
                <label htmlFor="code" className="block text-sm font-medium leading-6 text-gray-900">
                  Code
                </label>
                <div className="mt-2">
                  <textarea
                    id="code"
                    name="code"
                    rows={3}
                    className="block w-full rounded-md border-0 py-1.5 px-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                  />
                </div>
                <p className="mt-3 text-sm leading-6 text-gray-600">Anything you write here is passed to an <a className="text-sky-600" href="https://docs.python.org/3/library/functions.html#exec">exec</a> call on the server. The stdout will be displayed below.</p>
              </div>

              <div className="col-span-full gap-x-6">
                <button
                  type="submit"
                  className="float-right rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Submit
                </button>
              </div>

              <div className="col-span-full gap-x-6">
                <pre
                  className="text-sm"
                >
                  {output}
                </pre>
              </div>
            </div>
          </div>
        </div>

      </form>
    </main>
  )
}
