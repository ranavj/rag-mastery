"""
Day 9 — File 1: '|' pipe KHUD banao (samjho magic andar kya hai)
================================================================
LCEL ka `chain = a | b | c` koi jaadu nahi — sirf FUNCTION CHAINING hai.
Python mein `|` ko redefine kar sakte ho (operator overloading) — LangChain
ne yahi kiya. Hum bhi ek chhota Pipe banate hain.

Frontend analogy: RxJS `pipe(map, filter)` / Unix `cat | grep | sort` /
function composition. Data ek chhor se ghusta, har station kaam karke aage deta.
"""


# ---- ek chhota wrapper jo '|' ko "pipe" banata ----
class Step:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, x):          # step ko function ki tarah bula sako
        return self.fn(x)

    def __or__(self, other):        # <- YEH hai magic: a | b
        # "mera output doosre ko de do" -> ek naya Step return karo
        return Step(lambda x: other(self(x)))


# ---- kuch chhote steps (har ek ek kaam) ----
retrieve = Step(lambda q: f"[context for '{q}']")          # fake retrieve
make_prompt = Step(lambda ctx: f"PROMPT: answer using {ctx}")
call_llm = Step(lambda p: f"LLM_ANSWER({p})")
parse = Step(lambda ans: ans.replace("LLM_ANSWER(", "✅ ").rstrip(")"))


# ---- ab MAGIC: pipe se jodo ----
chain = retrieve | make_prompt | call_llm | parse
#       query -> context -> prompt -> llm -> clean answer

print("=== Scratch pipe (khud banaya) ===")
print("chain =", "retrieve | make_prompt | call_llm | parse\n")

result = chain("EMI bounce penalty?")
print(f"Input : 'EMI bounce penalty?'")
print(f"Output: {result}")

# ---- proof: yeh bilkul manual nesting jaisa hi hai ----
print("\n-- same cheez bina pipe (nested — ugly): --")
manual = parse(call_llm(make_prompt(retrieve("EMI bounce penalty?"))))
print(f"Output: {manual}")
print("\n🎯 Dono same! '|' sirf nesting ko SAAF likhne ka tarika hai.")
print("   parse(call_llm(make_prompt(retrieve(q))))  ==  retrieve | make_prompt | call_llm | parse")
