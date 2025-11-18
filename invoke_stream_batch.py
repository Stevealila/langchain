from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model("google_genai:gemini-2.5-flash-lite")
# response = model.invoke("What is science?")

# print(response.content)
# print("*"*80)

# for chunk in model.stream("What is science?"):
#     print(chunk.text)
# print("*"*80)

for batch in model.batch_as_completed([
    "Define AI",
    "Who was the most loved president of the USA?",
    "Tell me something about Steve Alila."
]):
    print(batch[1].content)
    print()
    print("*"*80)
    print()

'''
Steve Alila is a name that might ring a bell for many in the **Indonesian music scene**, particularly for those who were active or grew up in the late **1970s and 1980s**. He's primarily known as a **musician, singer, and songwriter**.

Here are some key things about Steve Alila:

*   **Member of Chaseiro:** His most prominent role was as a key member of the iconic Indonesian jazz-fusion band **Chaseiro**. Chaseiro was hugely influential in the Indonesian music landscape, known for their sophisticated arrangements, skilled musicianship, and innovative sound that blended jazz, funk, and Indonesian traditional elements. Steve Alila was a vocalist and songwriter within the band.

*   **Key Figure in Indonesian Jazz:** Along with Chaseiro, Steve Alila played a significant part in popularizing and evolving the jazz genre in Indonesia during a time when it was gaining more traction.

*   **Distinctive Vocal Style:** He had a recognizable and smooth vocal style that contributed to Chaseiro's signature sound.

*   **Songwriting Contributions:** He was also involved in writing songs for Chaseiro, contributing to their memorable repertoire.

*   **Continued Musical Pursuits:** Even after Chaseiro's initial active period, Steve Alila has continued to be involved in music, sometimes performing with Chaseiro or in other musical projects.

*   **Nostalgic Appeal:** For many Indonesians, Steve Alila and Chaseiro evoke a sense of nostalgia for a vibrant period in Indonesian music history.

In essence, Steve Alila is a respected figure in Indonesian music, primarily remembered for his contributions to the legendary jazz-fusion band Chaseiro, where he served as a vocalist and songwriter.

********************************************************************************

Pinpointing the "most loved" president is tricky because "love" is subjective and can be measured in different ways. There's no single, definitive answer that everyone would agree on. However, we can look at several indicators to get a sense of who might be considered among the most loved:

**Indicators of Presidential "Love":**

*   **Approval Ratings:** While approval ratings fluctuate throughout a presidency and are more about current satisfaction than long-term affection, consistently high approval ratings can be a strong indicator of broad public support during their term.
*   **Historical Reputation and Legacy:** How presidents are viewed by historians and the public decades or centuries later, often based on their accomplishments, character, and the impact of their policies.
*   **Public Memory and Nostalgia:** Some presidents become almost mythic figures in American consciousness, often invoked during times of national challenge or celebration.
*   **Enduring Popularity in Polls:** Modern polls sometimes ask about favorability or whether people would vote for past presidents if they could.

**Presidents Frequently Cited as "Most Loved" or Highly Regarded:**

Based on these indicators, a few presidents consistently rise to the top:

*   **Abraham Lincoln:** Despite the immense division of his time, Lincoln is almost universally revered for preserving the Union and ending slavery. His leadership during the Civil War, his eloquent speeches, and his perceived moral compass make him an enduring icon. His approval ratings during his presidency were often low due to the war, but his historical standing is exceptionally high.
*   **Franklin D. Roosevelt:** He led the nation through the Great Depression and World War II, implementing the New Deal and shaping the modern American state. His fireside chats fostered a sense of connection and reassurance. He won four presidential elections, a testament to his popularity.
*   **George Washington:** As the first president, he set many precedents and is seen as the "father of his country." His leadership during the Revolutionary War and his voluntary relinquishing of power are highly respected. He is a foundational figure in American identity.
*   **John F. Kennedy:** His presidency was tragically cut short, but his charisma, optimism, and vision, particularly during the Cuban Missile Crisis and the space race, left a lasting impression. He remains a symbol of hope and idealism for many.
*   **Ronald Reagan:** For a significant portion of the American population, Reagan is seen as a transformative president who revitalized the economy and played a key role in the end of the Cold War. His optimistic message and communication skills resonated deeply with many.

**Why it's Hard to Say for Sure:**

*   **Changing Times and Values:** What was considered "lovable" or admirable in one era might be viewed differently today.
*   **Political Polarization:** Presidents are often deeply divisive figures. What one group "loves," another might strongly dislike.
*   **Data Limitations:** We have more sophisticated polling data for modern presidents than for earlier ones.

**Conclusion:**

While there's no single "most loved" president, **Abraham Lincoln** and **Franklin D. Roosevelt** are arguably the strongest contenders based on their profound impact, enduring historical reverence, and the widespread admiration they command even today. **George Washington** is also in this elite group due to his foundational role. **John F. Kennedy** holds a special place in the hearts of many for his inspirational qualities.

Ultimately, who is "most loved" is a matter of personal perspective and the criteria one uses for evaluation.

********************************************************************************

Defining Artificial Intelligence (AI) can be approached from various angles, and there isn't a single, universally agreed-upon definition. However, we can provide a comprehensive understanding by looking at its core concepts, goals, and common interpretations.

Here's a breakdown of how to define AI:

**At its core, Artificial Intelligence (AI) refers to the development of computer systems that can perform tasks that typically require human intelligence.**

This broad definition can be further elaborated by considering:

**1. The "Intelligence" Aspect:**

*   **Cognitive Abilities:** AI aims to replicate or simulate human cognitive abilities such as:
    *   **Learning:** Acquiring knowledge and skills from data or experience.
    *   **Problem-Solving:** Identifying issues and devising solutions.
    *   **Decision-Making:** Choosing among different options based on available information.
    *   **Perception:** Interpreting sensory input (e.g., images, sounds, text).
    *   **Reasoning:** Drawing logical conclusions and making inferences.
    *   **Understanding Natural Language:** Processing and responding to human language.
    *   **Creativity:** Generating novel ideas or outputs.

**2. The "Artificial" Aspect:**

*   **Non-Biological Systems:** AI is created and implemented in machines, software, and algorithms, distinct from biological intelligence found in living organisms.

**3. The "Task Performance" Aspect:**

*   **Goal-Oriented:** AI systems are designed to achieve specific objectives or perform particular functions. These tasks can range from simple to highly complex.

**Common Interpretations and Categories of AI:**

Beyond the core definition, AI is often categorized and understood in different ways:

*   **Weak AI (Narrow AI):** This is the AI we see and interact with today. It is designed and trained for a **specific task**. Examples include:
    *   Virtual assistants (Siri, Alexa)
    *   Image recognition software
    *   Recommendation engines (Netflix, Amazon)
    *   Self-driving car systems
    *   Spam filters

*   **Strong AI (General AI or Artificial General Intelligence - AGI):** This is a hypothetical type of AI that possesses **human-level cognitive abilities across a wide range of tasks**. An AGI would be able to understand, learn, and apply its intelligence to any intellectual task that a human can. This remains a research goal and has not yet been achieved.

*   **Super AI (Artificial Super Intelligence - ASI):** This is a hypothetical AI that would **surpass human intelligence in virtually every field**, including scientific creativity, general wisdom, and social skills. This is even more speculative than AGI.

**Key Goals and Motivations Behind AI:**

*   **Automation:** To automate repetitive, mundane, or dangerous tasks.
*   **Efficiency and Productivity:** To improve processes and increase output.
*   **Problem Solving:** To tackle complex challenges that are difficult or impossible for humans to solve alone.
*   **Understanding Intelligence:** To gain insights into the nature of intelligence itself.
*   **Enhancing Human Capabilities:** To create tools that augment human abilities.

**In summary, AI is the field of computer science dedicated to creating systems that can perform tasks requiring intelligence, mimicking or exceeding human cognitive abilities in specific or general ways. While current AI is largely "narrow" and task-specific, the ultimate aspiration for many researchers is to achieve "general" AI, capable of human-level understanding and learning across diverse domains.**

********************************************************************************

'''