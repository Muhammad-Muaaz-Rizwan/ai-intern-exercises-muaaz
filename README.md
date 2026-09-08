# Transformer Day 1 Exercise

## 1. What is Generative AI?

Generative AI is basically a type of machine learning where the model doesn't just predict a label or a number — it actually creates new content. Text, images, audio, code, whatever. The way it works is the model looks at a huge amount of data during training and picks up on the underlying patterns/structure in it, and once it's learned that, it can sample from what it learned to produce something new that wasn't in the training set but still "fits" the patterns it saw. Most of today's GenAI (LLMs, image generators, etc.) is built on top of the Transformer architecture, trained on massive datasets.

**How it's different from traditional ML:**
Normal/traditional ML is mostly discriminative — meaning it learns a fixed mapping from input to output. Like, is this email spam or not, or what's the predicted price of this house. It's answering a "what is this" type question. GenAI flips that around and answers more of a "what could this be" question — it makes new data (a new sentence, a new image) that's statistically similar to what it trained on, but not copied from it. Also traditional ML usually needs labeled data for one specific task, while GenAI models are pretrained on tons of unlabeled data and can then be used for a bunch of different tasks afterward.

**3 real-world applications:**
- **Chatbots / text generation** — LLMs like GPT power things like ChatGPT, writing assistants, summarizers, code helpers, etc.
- **Image generation** — tools like Stable Diffusion or DALL and Googles Nano Banana·E can generate a full image just from a text prompt, used a lot in design and marketing now.
- **Code generation** — GitHub Copilot is a good example, it suggests/writes code based on the context you're already writing in.

---

## 2. Self-Attention Explained (With Example)

Consider the sentence:

```
"The cat sat on the mat"
```

The basic idea of self-attention is that every word in the sentence gets to "look at" every other word and figure out how much it should care about each one, to understand its own meaning better in that context.

**What are Query (Q), Key (K), and Value (V)?**
For every word, we generate three separate vectors by multiplying its embedding with three different learned weight matrices:
- **Query (Q):** think of this as the question the word is asking. Like "sat" is basically asking "who did this action, and where did it happen?"
- **Key (K):** this is what each word offers as a way to "answer" queries from other words — a label that can be matched against.
- **Value (V):** once a word's Key matches well with another word's Query, the Value is the actual info that gets pulled through.

Easiest way I think about it: Query = the question, Key = the label being matched against, Value = the actual content you get once there's a match.

**Why scale by √d_k?**
Attention scores come from taking the dot product of Q and K (QKᵀ). The problem is, as the dimension d_k gets bigger, these dot products can get really large in magnitude just by chance. When you feed really large numbers into softmax, it makes the output distribution extremely sharp/peaked (basically one-hot), and that kills the gradients during training — makes learning unstable. Dividing by √d_k just brings the scores back down to a reasonable range so training stays stable.

**Why apply Softmax?**
Softmax turns those scaled scores into an actual probability distribution — everything becomes positive and adds up to 1. That's what lets us say "this word should attend to word A 70% and word B 30%" instead of some random unbounded number. The more relevant a word is, the higher weight it gets, and these weights are what get used to blend the Value vectors together.

**What problem does this solve that RNNs had trouble with?**
RNNs go word by word, passing information forward through a hidden state. Two big issues come from this: first, long-range dependencies get lost — info from early words tends to fade out by the time you reach later ones (vanishing gradient problem), and second, since it's sequential, you can't parallelize training across time steps, so it's slow. Self-attention fixes both — every word can directly attend to every other word in one step regardless of how far apart they are, and since there's no step-by-step chain, the whole thing can be computed in parallel.

---

## 3. Encoder vs Decoder Comparison

| Component | Encoder | Decoder |
|---|---|---|
| **Primary role** | Reads and encodes the entire input sequence into contextual representations | Generates the output sequence one token at a time, using encoder context (if present) and previously generated tokens |
| **Attention direction** | Bidirectional — each token can attend to all tokens (past and future) in the input | Unidirectional (causal) — each token can only attend to itself and previous tokens |
| **Masked attention** | Not used | Used |
| **Cross-attention** | Not used | Used (in encoder-decoder architectures) |
| **Typical use case** | Understanding tasks — classification, embeddings, encoding context (e.g., BERT) | Generation tasks — text generation, translation output (e.g., GPT, decoder side of T5) |

**Masked attention:**
This only happens in the decoder. Basically it stops a token from "peeking" at future tokens that haven't even been generated yet — it does this by masking out (setting to −∞ before the softmax) any position that comes after the current one. This matters because the decoder is autoregressive, meaning it generates output one token at a time based only on what's already been generated, so training has to mimic that same left-to-right restriction.

**Cross-attention:**
This shows up in encoder-decoder setups and it's how the decoder gets to look at the encoder's output. The Queries come from the decoder side, but the Keys and Values come from the encoder side. So while generating each output token, the decoder can pull in relevant info from the entire input sequence (like the source sentence when translating).

**When each is used:**
- **Encoder-only** (like BERT) just uses regular bidirectional self-attention — good for understanding tasks/classification where you have the whole input upfront.
- **Decoder-only** (like GPT) only uses masked self-attention — makes sense since it's built for generating text.
- **Encoder-decoder** (like the original Transformer paper, or T5) uses all three types — bidirectional in the encoder, masked in the decoder, plus cross-attention connecting the two — this setup is good for sequence-to-sequence stuff like translation or summarization.

---

## 4. Vision Transformers (ViT) — High-Level Explanation

Vision Transformers basically take the same Transformer idea that was built for text and apply it to images, by turning the image problem into something that looks like a sequence modeling problem.

**What are image patches?**
You obviously can't feed an image into a Transformer pixel by pixel — that'd be a massive sequence and totally impractical computationally. So instead, ViT chops the image up into fixed-size square patches that don't overlap. So like a 224×224 image cut into 16×16 patches gives you 196 patches total. Each patch is basically treated like a "word" would be in a sentence.

**How do patches become tokens?**
Each patch (which is a small 2D chunk of pixels) gets flattened into a 1D vector, then run through a learnable linear layer that projects it into a fixed embedding size — this is pretty much the image version of a word embedding. Usually there's also a learnable [CLS]-style token stuck at the front of the sequence (same idea as BERT), and its output at the end is what's used for classification.

**Why do we need positional embeddings?**
Self-attention on its own has zero concept of order — it just sees a bag of tokens. But position clearly matters in an image; a patch of sky at the top of the image means something totally different than the same patch showing up at the bottom. So positional embeddings get added on top of each patch embedding to tell the model where in the image grid that patch actually came from.

**How's this conceptually different from CNNs?**
CNNs have a strong built-in bias toward images — local receptive fields, shared weights, pooling — basically assuming nearby pixels matter more to each other, and building up from small local features to bigger global ones layer by layer. ViT doesn't really assume any of that. Because of self-attention, every patch can interact with every other patch right from the first layer, no matter how far apart they are spatially. That gives ViT more flexibility to catch global relationships early, but the tradeoff is it needs a lot more training data to learn the spatial patterns that CNNs basically get for free from their architecture.
