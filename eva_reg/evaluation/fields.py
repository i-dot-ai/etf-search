# Note that this helptext supports markdown for formatting


from collections import defaultdict

create_help_text = defaultdict(
    str,
    {
        "title": "A full, descriptive title for the evaluation, include a name or description of the interventions being evaluated. Spell out any abbreviations unless they are very familiar (eg NHS).",
    },
)

description_help_text = defaultdict(
    str,
    {
        "brief_description": "One or two sentences describing the evaluation.",
        "topics": "One or more topics associated with this evaluation.",
        "organisations": "The organisation(s) responsible for this evaluation.",
    },
)


document_page_help_text = defaultdict(
    str,
    {
        "title": "Full title as it appears at the start of the document.",
        "document_types": "Select all types of information covered in this document.",
        "description": "Brief description of the document, if needed.",
        "url": "A link to a canonical version of the document somewhere on the web.",
    },
)


economic_design_help_text = defaultdict(
    str,
    {
        "economic_type": "Type of economic evaluation to be conducted.",
        "perspective_costs": "Which costs are to be included in the economic evaluation?",
        "perspective_benefits": "Which benefits are to be included in the economic evaluation?",
        "monetisation_approaches": "Approach(es) used to place monetary values on any costs or benefits that are not inherently expressed in monetary terms.",
        "economic_design_details": "Details of the design of the economic evaluation.",
    },
)


economic_findings_help_text = defaultdict(
    str,
    {
        "economic_summary_findings": "Short description (one to two sentences) of the findings related to the evaluation.",
        "economic_findings": "Longer description of the findings related to the evaluation, as required.",
    },
)


ethics_help_text = defaultdict(
    str,
    {
        "ethics_committee_approval": "Will the study be submitted to an ethics committee for approval?",
        "ethics_committee_details": "If the study will be submitted to an ethics committee, which one?",
        "ethical_state_given_existing_evidence_base": "Is the study ethically justified because there is uncertainty over which option is most beneficial? Or are there other reasons why conducting this study is ethical?",
        "other_ethical_information": "The headings on this record are not intended to cover all eventualities. Record any other ethical considerations here.",
    },
)


evaluation_cost_help_text = defaultdict(
    str,
    {
        "earliest_spend_date": "Earliest date on which this cost item might incur expenditure",
        "latest_spend_date": "Latest date on which this cost item might incur expenditure",
    },
)


event_date_help_text = defaultdict(
    str,
    {
        "event_date_name": "Select all types of information covered in this document.",
    },
)


grant_help_text = defaultdict(
    str,
    {
        "grant_details": "Provide any further details about this grant as required.",
    },
)


impact_analysis_help_text = defaultdict(
    str,
    {
        "impact_framework": "Type of comparisons between interventions.",
        "impact_basis": "Approach to identifying data to include in the analysis.",
        "impact_analysis_set": "Details of any inclusion / exclusion criteria determining data to be used in the analysis.",
        "impact_effect_measure_type": "Whether effects on outcomes are to be calculated / reported in absolute or relative terms.",
        "impact_primary_effect_size_measure": "Name of the measure to be used.",
        "impact_effect_measure_interval": "Interval calculation for the effect size.",
        "impact_primary_effect_size_desc": "Description of how the effect size measure and any associated interval are specified, including details of calculation if needed.",
        "impact_sensitivity_analysis": "Description of any sensitivity analysis",
        "impact_subgroup_analysis": "Description of any subgroup analysis",
        "impact_missing_data_handling": "Description of handling of missing data",
        "impact_fidelity": "Report to include information on the extent to which treatment was as protocol",
    },
)


impact_design_help_text = defaultdict(
    str,
    {
        "impact_design_name": "Descriptive name for the design/method. You may select more than one.",
        "impact_design_features": "Features making the evaluation more like 'real-world' implementation ('pragmatic attitude') vs 'perfect' conditions ('explanatory attitude').",
        "impact_design_equity": "Which disadvantaged subgroups (if any) have been identified for particular attention in the study and how?",
    },
)


impact_findings_help_text = defaultdict(
    str,
    {
        "impact_comparison": "Which intervention is being compared to which other?",
        "impact_outcome": "Which outcome measure is this comparison for? Should be one of the ones specified under outcome measures.",
    },
)


intervention_help_text = defaultdict(
    str,
    {
        "brief_description": "Brief description of intervention",
        "rationale": "Rationale, theory or goals of intervention elements.",
        "materials_used": "Description of physical or informational materials used in the intervention, including those used in intervention delivery or in training of intervention providers.",
        "procedures": "Description of each of the procedures, activities and/or processes used in the intervention, including enabling or supporting activities.",
        "provider_description": "Types of providers involved in providing the intervention, plus their skills, training, etc",
        "modes_of_delivery": "Description of modes of delivery (eg face-to-face, telephone) of the intervention and whether it will be provided individually or in a group.",
        "location": "Description of the type(s) of location(s) where the intervention will occur, including necessary infrastructure or relevant features.",
        "frequency_of_delivery": "Description of the number of times the intervention will be delivered and over what time period including the number of sessions, their schedule, and their duration or intensity. Number of sessions might be determined by some stopping criteria rather than a fixed number, in which case provide details.",
        "tailoring": "If the intervention will be personalised or adapted for different participants, description of what, why, when and how.",
        "fidelity": "Describe how closely the implementation of the intervention matches the implementation plan, including efforts to improve consistency.",
        "resource_requirements": "Describe extra resources added to (or resources removed from) usual settings in order to implement intervention.",
        "geographical_information": "In which actual locations (eg, towns, cities, or regions) will the intervention take place during the evaluation?",
    },
)


issue_description_help_text = defaultdict(
    str,
    {
        "issue_description": "The problem, circumstance or situation that it is intended that an intervention should respond to.",
        "those_experiencing_issue": "Those directly experiencing the issue.",
        "why_improvements_matter": "Why are the negative experiences a problem, or why would it be beneficial to achieve the prospective improvements?",
        "who_improvements_matter_to": "This may be wider than those experiencing the issue directly.",
        "current_practice": "How is the issue currently typically attended to (if at all)?",
        "issue_relevance": "How will the results of the evaluation ultimately contribute to practice?",
    },
)


links_help_text = defaultdict(
    str,
    {
        "links_name_of_service": "Which service is this an identifier for?",
        "links_link_or_identifier": "What is the link/identifier?",
    },
)


options_help_text = defaultdict(
    str,
    {
        "issue_description_option": "Do you want to complete an issue description for this evaluation?",
        "ethics_option": "Do you want to provide ethical information for this evaluation?",
        "grants_option": "Was this evaluation, or any of the interventions being evaluated, funded by a grant?",
    },
)


other_design_help_text = defaultdict(
    str,
    {
        "other_design_type": "Type of other evaluation to be conducted.",
        "other_design_details": "Details of the design of the evaluation.",
    },
)


other_findings_help_text = defaultdict(
    str,
    {
        "other_summary_findings": "A short description (one to two sentences) of the findings related to the evaluation.",
        "other_findings": "A longer description of the findings related to the evaluation, as required.",
    },
)


outcome_measure_help_text = defaultdict(
    str,
    {
        "name": "A name or brief phrase that describes the outcome.",
        "primary_or_secondary": "Will this outcome be treated as a primary or secondary outcome in this study?",
        "direct_or_surrogate": "Is this measure intended to directly reflect an outcome of interest or is it a surrogate measure that is intended to act as a proxy for an outcome that is hard to measure directly?",
        "description": "Details of what data will be gathered and of any processing that will be applied to raw data in order to create the measure.",
        "collection_process": "How will data be collected and by whom?",
        "timepoint": "When will data be collected?",
        "minimum_difference": "A difference or change in this outcome measure below this level would be considered negligible, unimportant or irrelevant.",
        "relevance": "Explain why the outcome and timepoint for measurement are considered important to evidence users.",
    },
)


participant_recruitment_help_text = defaultdict(
    str,
    {
        "process_for_recruitment": "Method of recruitment into the study, such as by referral, self-selection, or automatic inclusion of everyone in a category.",
    },
)


processes_standard_help_text = defaultdict(
    str,
    {
        "name": "If you have completed most fields in the Evaluation Registry, you will normally be able to claim at least partial conformity with the [Standard for producing evidence of the effectiveness of interventions (StEv2-1::2016)](https://repository.essex.ac.uk/32376/1/StEv2-1-2016%20Effectiveness-Specification.pdf)",
        "description": "Provide any information needed to describe the evaluation's conformity with the standard.",
    },
)


studied_population_help_text = defaultdict(
    str,
    {
        "studied_population": "Description of the population studied including settings and locations where the data are planned to be collected.",
        "eligibility_criteria": "A comprehensive description of the eligibility criteria used to select the study participants.",
        "sample_size": "The overall sample size of the evaluation. (Enter a number.)",
        "sample_size_units": "The units that the sample size is counted in.",
        "sample_size_details": "Details of the sample size and how the sample size was determined.",
    },
)


title_help_text = defaultdict(
    str,
    {
        "title": "A full, descriptive title for the evaluation, include a name or description of the interventions being evaluated. Spell out any abbreviations unless they are very familiar (eg NHS).",
    },
)


field_help_text = defaultdict(
    lambda: defaultdict(str),
    {
        "create": create_help_text,
        "description": description_help_text,
        "document": document_page_help_text,
        "economic-design": economic_design_help_text,
        "economic-findings": economic_findings_help_text,
        "ethics": ethics_help_text,
        "evaluation cost": evaluation_cost_help_text,
        "event date": event_date_help_text,
        "grant": grant_help_text,
        "impact-analysis": impact_analysis_help_text,
        "impact-design": impact_design_help_text,
        "impact-findings": impact_findings_help_text,
        "intervention": intervention_help_text,
        "issue-description": issue_description_help_text,
        "link": links_help_text,
        "options": options_help_text,
        "other-design": other_design_help_text,
        "other-findings": other_findings_help_text,
        "outcome measure": outcome_measure_help_text,
        "participant-recruitment": participant_recruitment_help_text,
        "process or standard": processes_standard_help_text,
        "studied-population": studied_population_help_text,
        "title": title_help_text,
    },
)

create_guidance_text = defaultdict(
    list,
    {
        "title": [
            "This should be a title for the evaluation as a whole, not for a given report or document associated with it, like 'Evaluation of the relative impact of ABC and DEF on XYZ outcomes' rater than 'Findings from an evaluation of ABC...' or 'Plans for an evaluation of ABC...'.",
            "This could include an indication of the evaluation type (eg impact evaluation) or method (eg randomised controlled trial) if known.",
        ],
    },
)

description_guidance_text = defaultdict(
    list,
    {
        "brief_description": [
            "This only needs to be a short summary as you will have the opportunity to provide more details elsewhere."
        ],
        "topics": [
            "The topics should be relevant to the target of the evaluation as well as those who might find this item relevant to their area of interest."
        ],
    },
)


document_page_guidance_text = defaultdict(
    list,
    {
        "document_title": [
            "If the document has no title, provide a descriptive title. It would be helpful if this provides an indication of both the type of document and the evaluation it relates to, eg 'Analysis plan for the evaluation of XYZ interventions'."
        ],
        "document_types": [
            "Information on an evaluation might be contained in one document or split across several. For example, in the planning stage a single document might contain both a study protocol and the analysis plan. And in reporting findings, technical details could be included in a separate document, but they could equally be included as appendices in a main report document.",
            "If a document contains elements that spans several of the document type options listed here, select all that apply.",
        ],
    },
)


economic_analysis_guidance_text = defaultdict(
    list,
    {
        "economic_analysis_description": [
            "Description providing sufficient detail that a suitably experienced person would be able to duplicate the analysis based on the information provided."
        ],
    },
)


economic_design_guidance_text = defaultdict(
    list,
    {
        "economic_type": [
            "The types of economic evaluation all aim to measure the comparative costs of interventions in monetary terms. They vary based on how they aim to report the outcomes.",
            "In **cost-minimisation analysis**, the interventions are known or assumed to provide the same outcome and the evaluation is intended to examine which of two (or more) interventions that cause the same outcome does so for the lowest cost.",
            "In **cost-effectiveness analysis**, the costs of delivering an intervention are compared to the amount of its outcome it achieves, in order to derive a cost-effectiveness ratio, which is expressed in terms of the cost for each unit of the outcome.",
            "In **cost-benefit analysis**, monetary values are placed on the benefits as well as the costs, in order to report a ratio that is expressed in the same terms (e.g. £2 of benefits for every £1 of expenditure).",
            "In **cost-utility analysis**, various outcomes are converted to a measure of 'utility', allowing the comparison of different outcomes on a common scale. This is commonly used in health sectors, where the most common measure of utility is the Quality Adjusted Life Year, QALY.",
            "If the economic evaluation is of a type not listed, select Other and specify the additional type(s).",
        ],
        "perspective_costs": [
            "The perspective is the point of view adopted when deciding which types of costs and benefits are to be included in an economic evaluation. Typical viewpoints are those of the person receiving the intervention, the organisation delivering the intervention, the wider public sector, or society. The broadest perspective is 'societal', which reflects a full range of social opportunity costs associated with different interventions.",
            "[ SOURCE: Adapted from Perspective, YHEC (2016) https://yhec.co.uk/glossary/perspective/ ]",
        ],
        "perspective_benefits": [
            "The perspective is the point of view adopted when deciding which types of costs and benefits are to be included in an economic evaluation. Typical viewpoints are those of the person receiving the intervention, the organisation delivering the intervention, the wider public sector, or society. The broadest perspective is 'societal', which reflects a full range of social opportunity costs associated with different interventions.",
            "[ SOURCE: Adapted from Perspective, YHEC (2016) https://yhec.co.uk/glossary/perspective/ ]",
        ],
        "monetisation_approaches": [
            "Some costs and benefits are naturally expressed in monetary terms. The natural measures for some others will not be in monetary terms, but may need to be monetised to fully include them in an economic evaluation. Provide details of any approaches used to monetise values that are not inherently expressed in monetary terms.",
            "You can also use this box to provide information on any costs or benefits that cannot be converted to monetary values.",
        ],
    },
)


economic_findings_guidance_text = defaultdict(
    list,
    {
        "economic_summary_findings": [
            "If the evaluation was of more than one type (for example, also an impact evaluation), record those findings in the relevant section and only use this section for the findings related to the 'economic evaluation' aspects of the evaluation."
        ],
    },
)


ethics_guidance_text = defaultdict(
    list,
    {
        "ethics_committee_approval": [
            "Not all studies need approval by an ethics committee.",
            "Ethics committee reviews are sometimes an obligation where a study could be considered health research; where a funder demands it; or where organisational processes require it.",
        ],
        "ethical_state_given_existing_evidence_base": [
            "Is there a state of uncertainty over which of the options being investigated is most beneficial (equipoise)? If not, are there other grounds making it ethical to offer a known-effective intervention to some and not others (for example, natural delay)?",
            "Is there an intervention that is already known to work for the issue being studied in this context? If so, is this being used as the comparison intervention for any new intervention being studied, rather than using a no-service comparison group?",
            "One of the main justifications for it being ethical to undertake a study is that there exists a state of ‘equipoise’ – ie that there is a degree of uncertainty about which of the options being compared is superior. If an intervention has already conclusively been shown to be effective then it would normally be ethically problematic to compare it to a control group receiving nothing. It would, however, still be acceptable to test it against another intervention of unknown effectiveness, or to compare it against ‘no treatment’ in a new context where it is not yet known whether the intervention would be effective.",
            "One exception to the requirement for equipoise can be a situation where there is a natural delay: where the intervention would be rolled out in a phased way to different beneficiaries anyway, then it can be ethical to conduct a study comparing those who get the intervention early against those who have not yet received it because they are due to get it later.",
        ],
        "risks_to_participants": [
            "Have you considered the risk of harm for participants, including any discomfort or inconvenience that they might experience through participation?"
        ],
        "risks_to_study_team": ["Have you considered risk of harm to those conducting the study?"],
        "participant_involvement": [
            "Have participants / potential participants been involved in the design of the study?"
        ],
        "participant_consent": [
            "Will consent be obtained? If not, why not?",
            "When will consent be obtained? Who will obtain consent?",
            "How will consent be given (eg verbal, written)? If not written, how will records be kept?",
            "What steps will be taken to ensure that consent is informed and freely given?",
            "If using secondary data, does the primary consent cover the proposed usage (for example, further analysis)?",
            "Attach a copy of the participant consent form, if being used.",
        ],
        "participant_information": [
            "What information will be provided to the participants about the study, its aims and procedures? Will any information be withheld? If so, why?",
            "Attach a copy of the participant information sheet, if being used.",
        ],
        "participant_payment": [
            "Will participants be paid? If so, how much? Has consideration been given to whether this creates a conflict of interest? How is the potential for that being mitigated in the design?"
        ],
        "confidentiality_and_personal_data": [
            "What steps will you take to protect the confidentiality of data of participants?",
            "Who will personally identifiable information be shared with?",
            "How will consent be obtained for use of personal data?",
            "How long will personal data be held for and how will it be disposed of?",
        ],
        "breaking_confidentiality": [
            "Are there circumstances under which confidentiality might be broken to prevent harm? If so, under what circumstances would this be done and what procedures would be used?"
        ],
    },
)


evaluation_cost_guidance_text = defaultdict(
    list,
    {
        "earliest_spend_date": [
            "If possible, provide at least approximate dates on when expenditure might be incurred in relation to this cost area. Even approximate dates, such as narrowing costs down to a year, will give future users a sense of whether they need to adjust these figures for inflation to intrepret them."
        ],
        "latest_spend_date": [
            "If possible, provide at least approximate dates on when expenditure might be incurred in relation to this cost area. Even approximate dates, such as narrowing costs down to a year, will give future users a sense of whether they need to adjust these figures for inflation to intrepret them."
        ],
    },
)


grant_guidance_text = defaultdict(
    list,
    {
        "grant_number": [
            "Provide the grant number or other similar unique identifier for this grant.",
            "For UK government grants, use the Government Grants Information System (GGIS) number.",
        ],
    },
)


evaluation_type_guidance_text = defaultdict(
    list,
    {
        "evaluation_type": [
            "Specify the type or types of evaluation this is.",
            "Do not use this field to specify the methods used; those are collected separately.",
            "An evaluation can be designed to be of more than one type, for example assessing both the effectiveness and the cost-effectiveness of the interventions being tested. If so, select all types of evaluation that are included.",
            "**Impact evaluations** are any evaluations that are intended to identify the effectiveness of interventions, including comparing different interventions against each other, or comparing a novel intervention against business-as-usual.",
            "**Process evaluations** are undertaken with the intention of increasing understanding of how an intervention is implemented, why it seems to work or not, and what contextual factors are affecting it, as distinct from whether an outcome was achieved.",
            "**Economic evaluations** (sometimes called value-for-money evaluations) are comparative analyses of alternative courses of action in terms of both their costs and consequences.",
            "If the evaluation includes types of evaluation not listed, select Other and specify the additional type(s).",
        ],
    },
)


impact_analysis_guidance_text = defaultdict(
    list,
    {
        "impact_framework": [
            "Is the study analysis designed to test for **superiority** (the intervention being better than the comparison), **non-inferiority** (the intervention being at least as good as the comparison) or **equivalence** (the intervention delivering the same outcomes as the comparison)?",
            "**Superiority** analysis is the most familiar framework. It is commonly used in the situation where a new intervention is being tested to see whether it out-performs current practice. It can also be used if variants of a new service are being tested to see which is the best.",
            "**Non-inferiority** analysis can be useful in situations such as when a new intervention has some other benefits (such as being cheaper or easier to deliver). In these cases, you might be happy to start using the new intervention as long as its outcomes are *no worse* than the existing situation.",
            "**Equivalence** analysis is most commonly used in a situation where you believe that two things should be the same and want to test that they are. These are used in situations such as a new manufacturer producing a version of a medicine and wanting to check that it delivers the same outcomes as existing versions of the medicine.",
        ],
        "impact_basis": [
            "There are options available for selecting whose data is included in the analysis of results, that may include or exclude people if they did not end up receiving the intervention they should have.",
            "**Intention-to-treat** analysis is an an assessment of the people (or other units) taking part in an evaluation, based on the group they were initially (and randomly) allocated to. This is regardless of whether or not they dropped out, fully adhered to the intervention or switched to an alternative intervention. Intention-to-treat analysis (ITT) analyses are often used to assess effectiveness because they mirror actual practice, when not everyone adheres to the intervention, and the intervention people have may be changed according to how their situation changes based on it.",
            "**Per-protocol** analysis is a comparison of groups in a trial that includes only those people (or other units) who completed the intervention they were originally allocated to. If done alone, this analysis leads to bias.",
            "SOURCE: Modified from NICE Glossary https://www.nice.org.uk/glossary?letter=i https://www.nice.org.uk/glossary?letter=p",
        ],
        "impact_effect_measure_type": [
            "Whether effects on outcomes will be calculated / reported in absolute or relative terms.",
            "**Absolute measures** are those that compare the levels of the outcomes between the groups as the *difference between them*. (Think, for example, of subtracting the baseline result from the achieved result.)",
            "**Relative measures** are those that compare the levels of the outcomes between the groups as *their ratios*. (Think, for example, of dividing the achieved result by the baseline result.)",
            "Absolute measures often provide a less distorted perception of the scale of impact of an intervention, so should generally be favoured as the primary form of measures. Consider, for example, a situation where business-as-usual results in 5% of people achieving some desired outcome and the novel intervention results in 15% of people achieving it. An absolute measure would be a prevalence difference of 10 percentage points. A relative measure would be a prevalence ratio of 3 : 1. Readers will typically get a clearer picture of the impact of the intervention from the absolute measure than the relative measure.",
        ],
        "impact_primary_effect_size_measure": [
            "For binary outcomes, a suitable absolute measure is often the 'prevalence difference': the difference between the proportions of people achieving the outcome in the intervention group and the control group. A relative measure for binary outcomes would be the 'prevalence ratio'.",
            "For numerical outcomes, suitable absolute measures often include differences in mean levels of the outcome between the groups. If the outcome is measured as a quantity that is meaningful in practice, the differences between mean levels of this quantity will also typically be something meaningful. (For example, if the outcome is each person's income in £ per week, then it will be meaningful and interpretable to see that weekly incomes are on average £x higher in the intervention group than the control group.)",
        ],
        "impact_effect_measure_interval": [
            "An interval should normally be calculated around the point estimate of the effect size to provide information about the level of uncertainty in that estimate or the range of values with which the data are relatively compatible.",
            "Consider, for example, a case where an evaluation finds that the point estimate for the effect of a financial intervention is that people receiving it end up with £100 per week more that people who do not. It is very helpful to know whether there is a large or small amount of uncertainty around that number. Are the data relatively compatible with values in the region £20 to £180, or only compatible with values from £95 to £105?",
            "Such intervals can also be used to create a summary interpretation of the effectiveness of an intervention, if such an interpretation is required. An interval that excludes zero (for example, +£10 to +£30) can be interpreted as the intervention being superior, whereas one that spans zero (for example, -£10 to +£20) is inconclusive.",
        ],
        "impact_interpretation_type": [
            "Intervals such as confidence intervals can be used to form an interpretation of findings. This will typically take the form of assessing whether the interval spans some null value or not. The null value is normally 0 (zero) for absolute measures and 1 (one) for relative measures. For example, if a confidence interval for the difference in mean weekly earnings between the intervention group and control group runs from +£5 to +£10, an interpretation of the interval might be that the intervention is superior for increasing earnings. If, however, the interval ran from -£5 to +£20, the interpretation might be that the findings are inconclusive (although both might be associated with the same point estimate for the difference).",
            "Hypothesis testing methods are often based on the calculation of p-values and the rejection of a null hypothesis if the p-value falls below some threshold (traditionally 0.05). These methods should generally be avoided as they are commonly misinterpreted.",
            "In some circumstances it might be appropriate to present findings from an evaluation in their numerical form (with associated measures of uncertainty) without attempting to reduce them down to a single interpretation.",
        ],
        "impact_subgroup_analysis": [
            "Subgroup analyses involve examining the results for a specified subset of the participants in a study. These should normally be specified before the study starts. If you are intending to conduct a subgroup analysis, it will normally be necessary to ensure that the sample size for that subgroup is large enough.",
            "Particular caution should be exercised over subgroup analyses that are specified after the data have been seen. A common mistake in studies is that if an intervention appears unsuccessful for the population as a whole, researchers can go 'fishing' through the data to find any subset of people it does work for. This is invariably a mistake because there will typically be some way of slicing the population that shows a positive outcome for one slice just due to random variation.",
        ],
        "impact_description_planned_analysis": [
            "Description providing sufficient detail that a suitably experienced person would be able to duplicate the analysis based on the information provided."
        ],
    },
)


impact_design_guidance_text = defaultdict(
    list,
    {
        "impact_design_justification": [
            "If an RCT design is specified, it is sufficient to note that it is appropriate, practical and ethical.",
            "If a design other than an RCT is specified, provide details of why an RCT was not appropriate.",
        ],
        "impact_design_description": [
            "Description providing sufficient detail that a suitably experienced person would be able to duplicate the study based on the information provided."
        ],
        "impact_design_features": [
            "Evaluation studies can be designed to have more focus on reflecting (potential) practice in the 'real world' or having more focus on identifying outcomes in 'perfect' (tightly controlled) conditions. These are called 'pragmatic attitude' and 'explanatory attitude', respectively. Studies normally sit somewhere on a spectrum between the two ends. For interventions that might be deployed in real practice, it is invariably more useful to have information from an evaluation that is more pragmatic in attitude rather than explanatory.",
            "Record design decisions taken to make the study more pragmatic in attitude. Detail any respects in which it was necessary to adopt an approach that is more explanatory in attitude.",
            "Studies should be designed to be pragmatic (as opposed to ‘explanatory’) in attitude. The intention with a pragmatic study is to establish whether the intervention is likely to work in real practice, whereas explanatory studies seek to identify whether an intervention can work in perfect conditions. Consequently, pragmatic studies are designed to resemble the situation in normal practice as closely as possible, rather than being delivered under tight controls. They would typically also be characterised by not having extremes of resources, training, or specialist staff conducting the intervention.",
        ],
        "impact_design_equity": [
            "Description of any design features, including data collection and analysis plans, that support the assessment of equity issues in the study.",
            "It may be possible to design a study that is able to address equity issues by identifying disadvantaged groups for subgroup analysis. One factor affecting the feasibility of this will be the available sample sizes, and whether it is possible to have enough participants from the subgroup identified to come to statistically significant conclusions.",
            "The PROGRESS-Plus mnemonic can be used to consider which disadvantaged groups could be focused on in the study, standing for Place of Residence, Race/Ethnicity, Occupation, Gender, Religion, Education, Socioeconomic Status, and Social Capital, and Plus represents additional categories such as Age, Disability, and Sexual Orientation.",
        ],
        "impact_design_assumptions": ["Any assumptions made as part of the design."],
        "impact_design_approach_limitations": [
            "Any limitations associated with the approach that are relevant to this study. For non-RCT designs this should include a description of any limitations of the approach’s ability to support robust causal inference."
        ],
    },
)


impact_findings_guidance_text = defaultdict(
    list,
    {
        "impact_comparison": [
            "If the evaluation has more than 2 interventions, will need to pick a pair; even if the evaluation only has 2 interventions, need to specify which is the base case and which is the 'tested' case"
        ],
    },
)


intervention_guidance_text = defaultdict(
    list,
    {
        "brief_description": [
            "One or two sentences to describe the intervention. This only needs to be a short summary as you will have the opportunity to provide more details elsewhere."
        ],
        "name": ["Name or brief phrase that describes the intervention."],
        "provider_description": [
            "For each category of intervention provider (eg housing officer) description of their expertise, background and any specific training they will receive."
        ],
        "fidelity": [
            "Description of how and by whom intervention fidelity (extent to which implementation is consistent with plan) will be assessed (if at all), and description of strategies that will be used to maintain or improve fidelity (if any).",
            "Indicate if efforts will be made to standardise the intervention or if the intervention and its delivery will be allowed to vary between participants, intervention providers, or study sites.",
        ],
    },
)


issue_description_guidance_text = defaultdict(
    list,
    {
        "issue_description": [
            "When studying interventions aimed at addressing a specific problem, you need to record the negative aspects of the situation that an effective intervention would improve.",
            "When studying an intervention that is untested but it is assumed that it would have a positive influence on one aspect of a situation you should record that aspect.",
        ],
        "why_improvements_matter": [
            "It is helpful to check that the identified issue is important and document why it is.",
            "For problems, this means establishing that the situation is actually bad. Sometimes the problem will be so clear and the intended outcomes so obvious that this step will just require a few sentences to document them; in other cases, considering this question will help to uncover assumptions that may not be shared by everyone involved in the intervention or study, or that need closer examination before they should be acted upon.",
            "Whilst many issues will be self-evidently problematic, in some cases it will not be so obvious whether an issue is actually perceived or experienced as a problem by those it affects. In these cases it may be worth undertaking a small piece of research with the affected population to check your intuition. This will typically require a piece of qualitative research, perhaps using interviews or focus groups.",
            "The same principles apply where the study is examining prospective improvements: sometimes the benefits will be immediately apparent; in other cases they should be examined to test that everyone would experience them as improvements.",
        ],
        "issue_relevance": [
            "What decisions are the results of this study intended to inform?",
            "Are there deadlines for making those decisions?",
            "How might practice be changed if an effective intervention is identified or an intervention is found to be ineffective?",
            "What information would this study need to generate to be able to affect these decisions?",
        ],
    },
)


options_guidance_text = defaultdict(
    list,
    {
        "issue_description_option": [
            "Select whether to complete a set of questions providing a structured description of the issue being investigated by the evaluation.",
            "An issue description helps to ensure that it is clear what questions the evaluation is intended to answer and why they are important. Without an issue description, it can be easy for the nature of the issue to remain an implicit and unstated assumption.",
            "The issue might be a specific problem or negative situation to be resolved or moderated, or it might be an improvement that it is hoped can be achieved.",
        ],
        "ethics_option": [
            "Select whether to complete a set of questions providing information addressing ethical considerations regarding the evaluation.",
        ],
        "grants_option": [
            "If there is grant funding, there will be an opportunity later for you to provide brief information about each relevant grant.",
        ],
    },
)


other_analysis_guidance_text = defaultdict(
    list,
    {
        "other_analysis_description": [
            "Description providing sufficient detail that a suitably experienced person would be able to duplicate the analysis based on the information provided."
        ],
    },
)


other_design_guidance_text = defaultdict(
    list,
    {
        "other_design_details": [
            "Use this box to describe your evaluation and how it will be conducted.",
            "Omit information about any impact evaluation, economic evaluation, or process evaluation aspects of the design. For those, make sure you have specified that you are undertaking that type of evaluation too, and then enter details about them on their respective pages.",
        ],
    },
)

other_findings_guidance_text = defaultdict(
    list,
    {
        "other_summary_findings": [
            "If the evaluation was of more than one type (eg, also an impact evaluation), record those findings in the relevant section and only use this section for the findings related to the 'other evaluation' aspects of the evaluation."
        ],
    },
)


other_measures_guidance_text = defaultdict(
    list,
    {
        "description": [
            "Details of what data will be gathered and of any processing that will be applied to raw data. This shall completely define the measurement such that others would be able to accurately replicate the measurement process based only on this information, including the format(s) the data will be collected, stored and/or presented in."
        ],
        "collection_process": ["How will data be collected, by whom, and when?"],
    },
)


outcome_measure_guidance_text = defaultdict(
    list,
    {
        "primary_or_secondary": [
            "The primary outcome measure will provide the principal assessment of whether the intervention is effective or not.",
            "It should be selected on the basis of being the best measure of the main outcome of interest in the study. It will also have special status in the study, for example in reporting the findings and in setting the sample sizes.",
            "As well as the primary outcome measure, secondary outcome measures can be selected for a number of reasons:",
            "- Establishing the effectiveness of intervention at delivering other benefits besides the primary target",
            "- Assessing the extent of any adverse outcomes",
            "- Monitoring the intermediate outcomes to assess the propagation of the impact of the intervention along the causal chain",
            "- Assessing the effectiveness of the intervention at timepoints other than the primary timepoint of interest",
            "- Collecting an alternative measure for compatibility with other studies.",
        ],
        "description": [
            "When defining the measure here, try to provide enough information such that others would be able to use it based only on this information.",
            "This will typically include the source of the data, as well as the format(s) the data will be collected, stored and/or presented in.",
        ],
        "timepoint": [
            "If specifying more than one timepoint, specify which of the timepoints is the primary timepoint of interest.",
            "Consider whether the data collection is before the intervention as well as after.",
        ],
        "minimum_difference": [
            "Where a new intervention is being studied, the minimum practically important difference might be informed by the amount by which it would have to outperform the existing standard approach to be worth considering deploying.",
            "As well as the difference itself, record how the number was arrived at. Establishing the minimum practically important difference may require a small qualitative piece of research with decision-makers in the implementing organisation to identify.",
            "Having an accurate impression of the minimum practically important difference is particularly important for the primary outcome as this will be the main factor affecting how large the sample sizes need to be for the study.",
        ],
    },
)


participant_recruitment_guidance_text = defaultdict(
    list,
    {
        "process_for_recruitment": [
            "Method of recruitment, such as by referral or self-selection.",
            "If recruiting by referral, where will referrals be accepted from? If recruiting by self-selection, where will the opportunity to participate be promoted?",
        ],
        "recruitment_schedule": [
            "If recording this information in the planning stages, describe the intended schedule. If recording it after that has concluded, record that actual schedule."
        ],
    },
)


processes_standard_guidance_text = defaultdict(
    list,
    {
        "name": [
            "Standards often have edition numbers, typically indicated by a year or a version number. Be sure to include the edition of the standard or process if the standard you are using has one, so it is clear which version of the standard you have followed. You should normally do this even if the version you are using is currently the only version, as there may be new versions in the future."
        ],
    },
)


visibility_guidance_text = defaultdict(
    list,
    {
        "visibility": [
            "Draft evaluations are only visible to the users assigned to it.",
            "Evaluations marked 'Civil Service' are visible to all civil servants.",
            "Evaluations marked 'Public' are visible to anyone. Before marking an evaluation as public, please ensure you have completed any processes in your organisation / department that are required for publishing.",
        ],
    },
)


studied_population_guidance_text = defaultdict(
    list,
    {
        "studied_population": [
            "Enter information on the population studied for the evaluation.",
            "In the case of some evaluations, this will be an identified group of people who will be allocated to receive (say) either a novel intervention or business-as-usual.",
            "In other cases, such as when you are evaluating a policy intervention that has been rolled out to a wide population and you aim to access administrative data on their outcomes, the studied population of the evaluation might be all the people whose data is included in the analysis.",
        ],
        "eligibility_criteria": [
            "The criteria should be justified and information provided on the degree to which they reflect the typical population that the intervention would be intended to be offered to if proven effective.",
            "The results of an evaluation are typically more useful if the participants included in the evaluation are as similar as possible to the population who would be intended to receive the tested intervention(s) outside of the evaluation, eg, the people who would receive the intervention if a policy were rolled out.",
            "Potential participants at substantially elevated risk of adverse outcomes from the intervention being studied should typically be excluded.",
        ],
        "sample_size": [
            "This will typically be the total number of people included in the evaluation. Provide any details below."
        ],
        "sample_size_units": [
            "This will normally be 'people' as each unit within an evaluation is a person. It can, however, be another unit if the population is of some other type.",
            "For example, if the results are per-school, the units might be 'schools'.",
            "For area-based evaluations, where aggregate outcomes for some areas are compared against outcomes for some other areas, the units might be 'areas', or some more specific version such as 'local authority areas', 'wards', or 'counties'.",
        ],
        "sample_size_details": [
            "For an evaluation that is comparing two or more interventions, this should include the number per 'arm' of the study (the number allocated to each intervention).",
            "If a calculation was used to determine the sample size, identify the primary outcome on which the calculation was based, all the quantities used in the calculation, and the resulting target sample size per arm.",
            "Details should be given of any allowance made for attrition or non-compliance during the study.",
        ],
    },
)


title_guidance_text = defaultdict(
    list,
    {
        "title": [
            "This should be a title for the evaluation as a whole, not for a given report or document associated with it, like 'Evaluation of the relative impact of ABC and DEF on XYZ outcomes' rater than 'Findings from an evaluation of ABC...' or 'Plans for an evaluation of ABC...'.",
            "This could include an indication of the evaluation type (eg impact evaluation) or method (eg randomised controlled trial) if known.",
        ],
    },
)


field_guidance_text = defaultdict(
    lambda: defaultdict(list),
    {
        "create": create_guidance_text,
        "description": description_guidance_text,
        "document": document_page_guidance_text,
        "economic-analysis": economic_analysis_guidance_text,
        "economic-design": economic_design_guidance_text,
        "economic-findings": economic_findings_guidance_text,
        "ethics": ethics_guidance_text,
        "evaluation cost": evaluation_cost_guidance_text,
        "evaluation-types": evaluation_type_guidance_text,
        "grant": grant_guidance_text,
        "impact-analysis": impact_analysis_guidance_text,
        "impact-design": impact_design_guidance_text,
        "impact-findings": impact_findings_guidance_text,
        "intervention": intervention_guidance_text,
        "issue-description": issue_description_guidance_text,
        "options": options_guidance_text,
        "other-analysis": other_analysis_guidance_text,
        "other-design": other_design_guidance_text,
        "other-findings": other_findings_guidance_text,
        "other measure": other_measures_guidance_text,
        "outcome measure": outcome_measure_guidance_text,
        "participant-recruitment": participant_recruitment_guidance_text,
        "process or standard": processes_standard_guidance_text,
        "visibility": visibility_guidance_text,
        "studied-population": studied_population_guidance_text,
        "title": title_guidance_text,
    },
)


def get_field_help_text(object_name, field_name):
    return field_help_text[object_name][field_name]


def get_field_guidance_text(object_name, field_name):
    return field_guidance_text[object_name][field_name]
