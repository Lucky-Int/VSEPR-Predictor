# VSEPR-Predictor
### Video Demo: <URL HERE>
### Introduction
VSEPR-Predictor (Valence Shell Electron Pair Repulsion - Predictor) is a cmd-line tool where a molecule is taken as input, and various different data is given as output-- mainly electron and molecular geometries, which then yields other info like hybridization-- with stepwise explanations as well. Calculating electron and molecular geometries *could* be done using quantum mechanics; however this project's aim is to create a viable tool for students or others who would like the learn how to use VSEPR theory tangibly.
### Process
The method used in this project is creating an abstract lewis structure of the molecule given, finding its central atom, terminal atoms . . . and most importantly its electron groups/clouds / steric number. Using the steric number or electron groups, and writing the molecule in VSEPR Form-- using the VSEPR Formula: $$AX_mE_n$$ -- the code then uses this formula and looks up its data in a dictionary.
#### Formula Breakdown
* **$A$** – **Central atom** .
* **$X$** – **Bonded/Terminal atoms** surrounding the central atom.
* **$m$** – **Number of bonded atoms**.
* **$E$** – **Lone pairs** of valence electrons on the central atom.
* **$n$** – **Number of lone pairs** (subscript number).

**Example**: A hypothetical molecule with a 4 Terminal atoms and 2 lone pairs would have a formula of **$AX_4E_2$** A subscript for X of 4 signifying 4 terminal atoms; a subscript of 2 for E signifying 2 Lone pairs for the central atom.

The code's dictionary essentially includes all of the data in the following table:
| VSEPR Formula | Steric Number | Bonding Groups ($m$) | Lone Pairs ($n$) | Electron Geometry | Molecular Geometry | Ideal Bond Angles | Hybridization |
| :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| $AX_2$ | **2** | 2 | 0 | Linear | Linear | $180^\circ$ | $sp$ |
| $AX_3$ | **3** | 3 | 0 | Trigonal Planar | Trigonal Planar | $120^\circ$ | $sp^2$ |
| $AX_2E$ | **3** | 2 | 1 | Trigonal Planar | Bent | $<120^\circ$ | $sp^2$ |
| $AX_4$ | **4** | 4 | 0 | Tetrahedral | Tetrahedral | $109.5^\circ$ | $sp^3$ |
| $AX_3E$ | **4** | 3 | 1 | Tetrahedral | Trigonal Pyramidal | $\sim107^\circ$ | $sp^3$ |
| $AX_2E_2$ | **4** | 2 | 2 | Tetrahedral | Bent | $\sim104.5^\circ$ | $sp^3$ |
| $AX_5$ | **5** | 5 | 0 | Trigonal Bipyramidal | Trigonal Bipyramidal | $90^\circ, 120^\circ$ | $sp^3d$ |
| $AX_4E$ | **5** | 4 | 1 | Trigonal Bipyramidal | Seesaw | $90^\circ, 117^\circ$ | $sp^3d$ |
| $AX_3E_2$ | **5** | 3 | 2 | Trigonal Bipyramidal | T-Shaped | $\sim90^\circ$ | $sp^3d$ |
| $AX_2E_3$ | **5** | 2 | 3 | Trigonal Bipyramidal | Linear | $180^\circ$ | $sp^3d$ |
| $AX_6$ | **6** | 6 | 0 | Octahedral | Octahedral | $90^\circ$ | $sp^3d^2$ |
| $AX_5E$ | **6** | 5 | 1 | Octahedral | Square Pyramidal | $\sim90^\circ$ | $sp^3d^2$ |
| **$AX_4E_2$** | ***6*** | **4** | **2** | **Octahedral** | **Square Planar** | **$90^\circ$** | **$sp^3d^2$** |

(***Table Generation and syntax help from AI***)

Therefore, from our example above-- of the molecule with formula **$AX_4E_2$**-- by looking at the table (last row, bolded), we can see that the molecule has a steric number of 6, an Octahedral Electron Geometry, Ideal bond angles of 90 degrees. . . and more (to be explained).

### *How does the code figure out the respective VSEPR Form of a given molecule?* (Process Cont.)
As stated, an abstract lewis structure is created, and then electron configurations and the data we need are figured out from there. How, specifically, is this figured out using VSEPR-Predictor? First of all, the code parses input, only taking in actual molecules (using the python library *chemicals* as assist), and creates a list of dictionaries which includes element names and their subscripts. An example for H2O is shown here:
```json
[
  { "Element": "H", "Subscript": "2" },
  { "Element": "O", "Subscript": "1" }
]
```
Hydrogen (H) has a subscript of 2, and Oxygen (O) has a subscript of 1, which matches the properties of $\text{H}_2\text{O}$. (Notice how element O has a subscript of 1 although $\text{H}_2\text{O}$ isn't necessarily written as $\text{H}_2\text{O}_1$; parsing, similar and more messy than this, is important for the function of the project. When writing the code, I thought this part would be relatively easy, however it was harder for me than it looked. Although the code itself for this part isn't that complex, it took me a lot of trial and error to perfect it.)

Using this data, the code then uses a library (mendeleev) for data of valence electrons of constituent atoms, which is just periodic table data. Simple algorithmic and mathematical code then multiplies each valence electron count by the subscript of each respective element, and then adds everything together to yield the total valence electrons. What is relatively more difficult is calculating Valence Electrons of polyatomic ions and molecules with charges. Not that the math becomes any more difficult, however the parsing does. In this way, the aforementioned code could fail due to confusions between subscripts and charges and a lot of other edge cases. A clean approach to this is to use regular expressions (re) to find the charge syntax and then parse. Then, the charges are accounted for and valence electrons are counted correctly. The specific regex is shown below:

**`r"(\d)?(\d)?(\+|-)$"`**

Using the instance above, we see that $\text{H}_2\text{O}$ has **2 hydrogens** and **1 oxygen**.

The code then sees that hydrogen has **1 valence electron** and oxygen **6**, using the following code:

`get_element(element).nvalence()`

*(where `element` is $\text{H}_2\text{O}$ or a parsed version).*

 It is, perhaps, **important to note** that-- although the project uses VSEPR Theory which yields data depending on the central atom, and that this project allows only molecules with a one defined central atom for simplicity (for now)-- this calculation of valence electrons **works for *all* molecules**, including those with multiple central atoms, for example methanol ($\text{CH}_3\text{OH}$). The total valence count is **very** useful; as, it is one of the main pillars of the following code.

 #### Abstract Lewis/Dot Structure (partially)
 The code then creates a sort of dot or lewis structure, just abstractly. The code follows a similar way of creating the structure to how you would create it in real life-- however, just more difficult and verbose. It's worth noting that this code does not create the hypothetical double and triples bonds for the respective molecule. This is because, as you can imagine, **we only need the** calculations for the lone pairs and **electron groups** in general. The approach taken is to take account of the total valence electrons we have, and then to account for some and subtract from the total, the goal being 'use up' all of our valence electrons.

 ##### **Simplified Order of Steps**
The following are the simplified order of steps for the `fetch_structure_data(elements_and_nums, ve_total, central_atom,)` function

1. **Create covalent bonds** from the central atom to terminal atoms (2 per). This is the same as 2 times the number of terminal atoms. We then subtract this from the total amount of valence electrons and update the number. If the number of valence electrons is already 0, we are done.
2. **If we still have 'leftover valence electrons'**, which is in a lot of cases, we can spread the valence electrons upon each terminal atom so they all reach 8 valence electrons. If there are no more valence electrons to account, we are done-- at least for our purposes (read section above^^^).
3. **If we still have 'leftover valence electrons'**, we will then assign the central atom with all of them in lone pairs, 2 per pair. We should likely have no more valence electrons, and we would be done-- again, for our purposes (read section above^^^).

> **Note:** Of course, all of this is done abstractly; and technically speaking, there is no actual Lewis or dot structure being created-- all of this information is just stored in variables and other data types. **That being said,**, this code and these variables can still be used to draw or create a model of a lewis or dot structure (which is in my future plans for the project).

And there we have it: the electron groups and lone pairs around the central atom, essential for using VSEPR Theory. The code then writes the molecule's properties in VSEPR Form (read **Process**, 1st section under introduction.) If you didn't know, the amount of lone pairs, although it doesn't change the amount of electron groups we have, is needed because they take up more space and have stronger coulomb forces (they repel other electrons more). Therefore, the shape changes and that needs to be accounted for. Note that, there is no logic like this for double or triple bonds, so they do not matter for our purposes.

#### **Summary and Conclusion**
VSEPR Predictor is a project that very mathematically and algorithmically calculates electron groups and lone pairs, needing prerequisite information to figure that out, and also yielding extra information like bond hybridization as well. The approach, abstractly, is similar to how you would use VSEPR Theory on-paper. However, the logic must be written differently and 'translated' into code. This way, the project was perfect for a first project to practice my skills, as it becomes a sort of challenge.




