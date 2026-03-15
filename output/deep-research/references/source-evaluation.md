# Source Credibility Evaluation Framework

Use this framework to rate the credibility of sources found during research. This is an enhanced version that includes citation-mismatch detection — the most common failure mode in AI research systems.

## Credibility Tiers

### HIGH Credibility
- Peer-reviewed journal articles (Nature, Science, The Lancet, JAMA, etc.)
- Official government data and reports (WHO, CDC, Bureau of Labor Statistics, etc.)
- Official documentation and specifications (RFCs, W3C specs, API docs)
- Established news outlets with editorial standards (Reuters, AP, BBC, NYT, WSJ)
- Reports from recognized institutions (World Bank, IMF, Brookings, RAND)
- Primary sources (original research papers, official announcements, court filings)

### MEDIUM Credibility
- Reputable industry blogs and publications (TechCrunch, Ars Technica, The Verge)
- Conference presentations and proceedings
- Well-cited preprints (arXiv, SSRN) with significant engagement
- Industry reports from consulting firms (McKinsey, Gartner, Forrester)
- Expert blog posts from recognized domain authorities
- Wikipedia (good starting point — follow citations to primary sources)
- Well-maintained open-source project documentation

### LOW Credibility
- Personal blogs without clear expertise
- Social media posts (Twitter/X, Reddit, etc.)
- Forum discussions (Stack Overflow answers are useful but verify)
- Undated content with no clear authorship
- Anonymous sources
- Content from content farms or SEO-optimized sites
- AI-generated content without human editorial review

### RED FLAGS (treat with extreme caution)
- No author attribution
- No publication date
- Promotional or sponsored content presented as editorial
- Contradicts multiple reliable sources without strong evidence
- Domain registered recently with no track record
- Claims extraordinary results without peer review
- Uses emotional language rather than evidence-based arguments

## Citation-Mismatch Detection

The most common failure mode in AI research is **citation mismatch** — the URL is real, but the claim attributed to it is fabricated or distorted. Watch for:

1. **Specific numbers attributed to a source**: If an agent claims "Source X says 47% of..." — the number may be fabricated even if Source X is real
2. **Quotes that seem too perfect**: Exact quotes that perfectly support the argument may be paraphrased or invented
3. **Claims that are too specific**: Vague claims are less likely to be mismatched than hyper-specific ones
4. **Multiple agents citing the same URL for different claims**: Cross-check — the URL may only support one of them

**Mitigation**: When a critical claim rests on a single source, assign it LOW confidence regardless of source credibility tier, and flag it for Round 2 verification.

## Quick Assessment Checklist

When evaluating a source, check:
1. **Who wrote it?** — Can you identify the author and their credentials?
2. **When was it published?** — Is the information current?
3. **Where is it published?** — Does the platform have editorial standards?
4. **Why was it written?** — Is it informational, or trying to sell something?
5. **How is it supported?** — Does it cite its own sources?
6. **Who else says this?** — Do independent sources corroborate?

## AI-Source Detection

With an estimated 85% of web content now machine-generated, be alert to:
- Content that reads fluently but lacks specific details or original insights
- Articles that aggregate without adding analysis
- Sources that circularly cite other AI-generated content
- Lack of first-person experience, original data, or unique perspective

When in doubt, prefer sources with clear human authorship, original research, or institutional backing.
