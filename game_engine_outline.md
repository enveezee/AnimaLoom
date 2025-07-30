
# Kismet Engine: Comprehensive Design Outline

## 1. Core Philosophy: The "Tangled Web"

The central design goal is to create a **human behavior simulator** for generating emergent narratives. The engine will prioritize deep character simulation over simple, deterministic game loops. The core principle is that character actions are not just events, but consequences of a complex interplay between personality, emotional state, relationships, and needs. The system should be abstract enough to represent any "agent" (a character, a faction, a creature) that can interact with the world.

## 2. The Agent: An Abstract Model of Action

At the highest level, the game is populated by **Agents**. An "Agent" is any entity capable of independent action and possessing a set of defining characteristics. This could be a person, an animal, a monster, or even an organization.

### 2.1. Agent Core: The Unchanging Self (Relatively)

These are the fundamental, slow-to-change aspects of an Agent.

*   **Archetype/Class:** A template defining an Agent's role or function (e.g., "Diplomat," "Warrior," "Merchant," "Apex Predator").
    *   Provides baseline attribute modifiers.
    *   Determines initial "Deck" composition (see Section 4).
    *   May grant unique, passive abilities.
*   **Core Attributes:** The raw stats defined in `game_config.toml`. These are the Agent's fundamental capabilities.
    *   *Physical:* Strength, Agility
    *   *Mental:* Intellect, Perception
    *   *Social:* Charisma, Composure
    *   *Internal:* Resilience, Passion
*   **Personality Traits (The OCEAN Model):** The Agent's innate psychological profile. This is the primary driver of "tendencies."
    *   **Openness:** Influences desire for novel actions/cards ("Explore," "Create").
    *   **Conscientiousness:** Influences preference for planned actions, resource management.
    *   **Extraversion:** Governs the "Social Battery" and preference for social cards.
    *   **Agreeableness:** Influences the ratio of positive vs. negative social cards.
    *   **Neuroticism:** Affects susceptibility to negative emotional states and `Sanity` degradation.

### 2.2. Agent State: The Fluctuating Self

These are the dynamic, moment-to-moment conditions of an Agent.

*   **Emotional State:** The Agent's current mood (e.g., Joyful, Sad, Angry, Scared).
    *   Directly modifies the success chance of certain actions (e.g., `Anger` boosts `Intimidate` but penalizes `Persuade`).
    *   Can temporarily add or disable cards in the Agent's "Hand."
    *   Can be influenced by external events or internal `Needs`.
*   **Needs & Motivations (Maslow-esque Hierarchy):** The Agent's underlying drivers. An Agent will be biased towards actions that fulfill their most pressing need.
    *   **Security:** (Health, Resources, Shelter) -> Drives actions like "Forage," "Barter," "Find Shelter."
    *   **Belonging:** (Social Connection) -> Drives use of `Platonic` and `Romantic` cards.
    *   **Esteem:** (Respect, Status) -> Drives use of `Admired` and `Rivalrous` cards.
    *   **Self-Actualization:** (Personal Growth) -> Drives use of skill-gain or creative cards.
*   **Derived/Secondary Attributes:** Calculated stats that provide a snapshot of the Agent's well-being.
    *   **Health/Stamina:** Physical well-being.
    *   **Sanity/Willpower:** Mental well-being.
    *   **Social Battery:** Capacity for social interaction.
    *   **Reputation:** Social standing.

### 2.3. Agent Knowledge & History: The Remembered Self

This is the Agent's memory and awareness, the source of context for its actions.

*   **Affinity Metrics:** The directional relationship graph. How this Agent feels about every other Agent.
*   **Hidden Stats & Resources:**
    *   **Secrets:** A list of known, sensitive information.
    *   **Grievances:** A record of slights and injustices suffered.
    *   **Social Capital:** A measure of favors owed and given.
    *   **Trauma:** A counter for significant negative events.
*   **Known Information:** Facts about the world, other agents, and objectives.

## 3. The Action System: Cards as Abstract Intent

**Cards** are the engine's representation of **intent**. They are not just "attacks" or "spells," but any discrete action an Agent can choose to perform. The "deck" is the full set of an Agent's possible actions, and their "hand" is what they can do *right now*.

### 3.1. Card Anatomy

As defined in `card_creation_guide.md`, but with a focus on abstraction:

*   **Name:** The action (e.g., "Share a Secret," "Forage for Food," "Declare War").
*   **Challenge:** The core attribute(s) being tested.
*   **Effect:** The potential outcomes. This is where the "tangled web" comes into play.

### 3.2. The "Tangled" Challenge Roll

The core of the simulation. A simple `Actor vs. Target` roll is replaced by a multi-stage calculation:

1.  **Base Roll:** `Actor's [Challenge Attribute] + Randomizer` vs. `Target's [Defense Attribute] + Randomizer`.
2.  **Contextual Modifiers (The "Tangle"):** The base roll is then heavily modified by:
    *   **Emotional State:** Is the Actor `Angry`? +5 to Intimidation. Is the Target `Sad`? -5 to their defense.
    *   **Personality:** Is the Actor highly `Agreeable`? -10 to all `Antagonistic` actions.
    *   **Affinity:** Does the Actor have high `Platonic` affinity for the Target? Bonus to "Help" actions, penalty to "Harm" actions.
    *   **Needs:** Is the Actor's `Security` need critical? Bonus to "Forage" or "Steal" actions.
    *   **History:** Does the Actor have a `Grievance` against the Target? Massive bonus to antagonistic actions.

3.  **Outcome Determination:** The final, modified roll determines the outcome. Outcomes can be more complex than simple success/failure:
    *   **Critical Success:** A surprisingly positive result.
    *   **Success:** The intended effect.
    *   **Partial Success:** The intended effect, but with a cost.
    *   **Failure:** The action has no effect.
    *   **Critical Failure (Backfire):** The action has a negative effect on the Actor.

## 4. The World: Environment & State

*   **Game World State:** A collection of all Agents and their current states.
*   **Map/Location:** The current environment, which can have its own properties (e.g., "Dangerous," "Public Place") that affect actions.
*   **Time:** A system for tracking time, allowing for day/night cycles, seasons, and the passage of years, which can influence Agent needs and actions.

## 5. Data Structure & Implementation

*   **`game_config.toml`:** The canonical source for all base attributes, affinities, and card properties.
*   **`cards.toml` / `agents.toml`:** Separate TOML files for defining the specific cards and agent archetypes available in a given game module.
*   **SQLite Database:** A runtime representation of the **current game state**. It stores the dynamic data: the specific instances of Agents, their fluctuating states, relationships, and inventory. It is generated from the TOML files at the start of a new game.
*   **Python Classes:**
    *   `Agent`: A class to hold all the data for a single agent instance.
    *   `Card`: A class for card data.
    *   `Encounter`: A class to manage the interaction between two or more agents, containing the "Tangled Challenge Roll" logic.
    *   `WorldState`: A singleton class that holds all active agents and the global game state (time, etc.).

This outline provides a framework for building the complex, interconnected system you've described. It emphasizes the simulation of character psychology as the primary driver of gameplay, which should lead to the rich, emergent narratives you're aiming for.
