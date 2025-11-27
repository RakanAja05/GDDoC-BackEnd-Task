const messagesEl = document.getElementById('messages')
const questionEl = document.getElementById('question')
const sendBtn = document.getElementById('send')

function appendMessage(text, who='bot'){
  const div = document.createElement('div')
  div.className = 'msg ' + (who==='user' ? 'user' : 'bot')
  // use a paragraph for content so longer text wraps nicely
  const p = document.createElement('div')
  p.className = 'msg-content'
  p.innerText = text
  div.appendChild(p)
  messagesEl.appendChild(div)
  // keep the newest message in view
  messagesEl.scrollTop = messagesEl.scrollHeight
}

async function send(){
  const q = questionEl.value.trim()
  if(!q) return
  appendMessage(q, 'user')
  questionEl.value = ''

  const payload = {
    question: q,
    system: 'You are a friendly assistant that answers in Indonesian, concise and polite.',
    // always use the 'rakan' persona for consistent first-person replies
    user_profile: {},
    as_persona: true,
    persona_preset: 'rakan'
  }

  // ensure we have a conversation token in localStorage
  let convToken = localStorage.getItem('conversation_token')
  if(!convToken){
    try{
      const createRes = await fetch('/api/conversations', { method: 'POST' })
      const createData = await createRes.json()
      convToken = createData.token
      localStorage.setItem('conversation_token', convToken)
    }catch(e){
      console.warn('Could not create conversation token, proceeding without persistence', e)
    }
  }
  if(convToken) payload.conversation_token = convToken

  appendMessage('Menjawab...', 'bot')
  try{
    const res = await fetch('/api/chat', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) })
    const data = await res.json()
    // remove last placeholder bot message
    const last = messagesEl.querySelector('.msg.bot:last-child .msg-content')
    if(last && last.innerText==='Menjawab...'){
      // replace placeholder text with actual reply
      last.innerText = data.reply || 'Tidak ada jawaban'
    } else {
      appendMessage(data.reply || 'Tidak ada jawaban')
    }
  }catch(e){
    console.error(e)
    appendMessage('Gagal menghubungi server. Cek konsol.', 'bot')
  }
}

sendBtn.addEventListener('click', send)
questionEl.addEventListener('keydown', (e)=>{ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); send() } })

// persona is automatic; no UI controls needed
