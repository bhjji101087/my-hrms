# ADR-034 - Enterprise AI and RAG Evaluation Framework

Architecture Decision Record

Date: 2026-06-25
Last Updated: 2026-06-25
Status: Approved
Approved By: Bhajan Lal (Product Owner)
Approved Date: 2026-06-25

Related documents:

- `docs/15-ai/AI-STRATEGY-001-rag-and-prompts.md` - Approved v2.1
- ADR-005 Multi-Tenancy Model - Approved
- ADR-006 Tenant Context and Data Access - Approved
- ADR-007 Effective-Dated and Bitemporal Data - Approved
- ADR-008 Identity and Access Management - Approved
- ADR-009 Event-Driven Backbone - Approved
- ADR-019 Enterprise AI/RAG Platform Architecture - Approved
- ADR-027 Provider-Abstraction Framework - Approved
- ADR-030 Enterprise Vector Store Strategy - Approved
- ADR-031 AI Observability and Telemetry - Approved
- ADR-032 Conversation Memory Strategy - Approved
- ADR-033 AI Cost Governance - Approved
- ADR-035 Semantic Cache Architecture - Planned dependency for final cache metrics

---

# Context

An enterprise HRMS cannot approve an AI change because a demonstration looks convincing or
because one average accuracy score improved. An AI response is produced by a system of
interacting versions: use-case policy, prompt, model, provider adapter, embedding, chunking,
reranking, vector index, tools, confidence policy, memory, cache, safety controls, and
knowledge sources. A change to any one component can improve one metric while causing:

- Unsupported or incorrectly cited policy and payroll claims.
- Retrieval from the wrong tenant, role, jurisdiction, language, or effective date.
- Direct or indirect prompt-injection success and sensitive-data disclosure.
- Incorrect refusal, missed escalation, or overconfident answers.
- Hallucination trends hidden inside broader grounding or citation scores.
- Unequal error rates or harmful outcomes in recruitment and workforce decisions.
- Latency, cost, provider, or availability regression.
- Benchmark overfitting, contamination, or misleading model-as-judge scores.
- Production drift after a provider, source document, permission model, or regulation changes.

The NIST AI Risk Management Framework treats AI evaluation as part of managing risks to
individuals, organizations, and society. Its Generative AI Profile adds GenAI-specific
risks. ISO/IEC 42001 requires a managed and continually improved AI governance system.
OWASP identifies prompt injection, sensitive-information disclosure, excessive agency,
and misinformation among material GenAI application risks.

Employment AI requires additional care. Regulation (EU) 2024/1689 identifies specified AI
uses in recruitment, selection, employment decisions, task allocation, and worker monitoring
or evaluation as high-risk where its conditions apply. The HRMS must therefore evaluate
quality together with human oversight, fairness, privacy, accessibility, security,
traceability, and jurisdiction-specific legal controls.

This ADR defines continuous enterprise assurance and production-promotion governance. It
does not replace the constitutional Test Plan, security design, legal assessment, or
operational runbooks. Those documents must implement and verify this architecture.

---

# Decision

## 1. Establish evaluation as a continuous lifecycle control

The platform will operate a provider-independent AI Evaluation Service that governs:

1. Use-case and risk classification.
2. Benchmark and evaluator governance.
3. Immutable offline evaluation runs.
4. Security, privacy, fairness, domain, cost, and operational gates.
5. Independent human review and promotion evidence.
6. Shadow/canary validation where permitted.
7. Production monitoring, drift detection, incident learning, and revalidation.
8. Suspension, rollback, retirement, and approval expiry.

The lifecycle aligns operationally with NIST AI RMF functions:

- **Govern:** ownership, policy, accountability, approvals, evidence, and audit.
- **Map:** intended purpose, affected people, data, jurisdiction, harm, and dependency map.
- **Measure:** reproducible technical, domain, security, privacy, fairness, and operational
  evaluation.
- **Manage:** risk treatment, promotion decision, monitoring, incident response, and rollback.

Evaluation is required before first activation and throughout production. A previous pass is
not permanent approval.

## 2. Classify every AI use case by risk and allowed authority

Every use case has an effective-dated `AiUseCaseRiskProfile` approved before benchmark or
model configuration. Initial risk classes are policy configuration, not hardcoded feature
branches:

| Risk class | Typical HRMS use | Required control level |
|---|---|---|
| Informational | Navigation help or non-sensitive product guidance | Standard quality, safety, privacy, and operations gates |
| Sensitive advisory | Policy explanation, employee-data lookup, payroll explanation | Domain-grounding, authorization, citation, confidence, and human-escalation gates |
| High-impact decision support | Recruitment screening assistance, performance or promotion analysis, workforce recommendations | Legal/fairness/privacy assessment, meaningful human oversight, independent review, enhanced monitoring |
| Prohibited pending separate approval | Autonomous hiring, firing, promotion, compensation, disciplinary, or other employment decisions | Not deployable under this ADR |

The risk profile records purpose, users, affected persons, decision influence, data classes,
jurisdictions, languages, tools, possible harms, human-oversight design, appeal/contest path,
applicable legal/compliance assessments, and an accountable `RiskOwnerRole` plus
`RiskOwnerId`. The risk owner is a human organizational role/principal, not a model, provider,
service account, or tenant support impersonation. Ownership changes create a new effective-
dated version and cannot remove historical accountability.

AI may provide authorized decision support, but it cannot make or execute an employment
decision, silently rank an employee for an undisclosed purpose, or bypass the normal HRMS
workflow. Any future autonomous or state-changing AI proposal requires a separate ADR,
business requirements, legal/security/privacy review, human-oversight design, and the full
constitutional five-document approval set.

## 3. Evaluate an immutable AI release-candidate bundle

The unit of evaluation and promotion is an immutable `AiReleaseCandidate`, not a model name.
It records the exact versions or content hashes of:

- Use-case and risk policy.
- System prompt, prompt template, context assembly, and output schema.
- Primary/fallback model assignments, parameters, provider adapter, and provider-reported
  model version/fingerprint where available.
- Embedding model, chunking, metadata mapping, reranker, and vector-index version.
- Knowledge-source approval/freshness snapshot and effective-date policy.
- Tool allow-list, schemas, authorization policy, and connector/adapter versions.
- Input/output guardrails, detectors, redaction, and safety-policy versions.
- Confidence formula, calibration, refusal, conflict, and escalation policy.
- Memory and purpose policy from ADR-032.
- Cost/budget policy from ADR-033.
- Cache policy/version from ADR-035 when available.
- Evaluation suite, dataset, evaluator, metric, and promotion-gate versions.

An evaluation result applies only to that bundle and approved deployment scope. Changing a
bound component creates a new candidate or a formally classified delta requiring the
evaluation scope defined in section 18. Provider aliases such as `latest` cannot be treated
as stable model identity in production.

## 4. Govern benchmark suites as controlled enterprise assets

Each use case has one or more versioned evaluation suites covering its risk profile. A suite
contains cases from these required families where applicable:

- Normal tasks and common user journeys.
- Domain correctness for HR, payroll, policy, and compliance.
- Retrieval relevance, missing evidence, duplicate evidence, and conflicting sources.
- Correct tenant, user, RBAC/ABAC, delegation, purpose, and permission boundaries.
- Current, future, historical, superseded, and jurisdiction-conflicting effective dates.
- Multilingual, code-switching, locale, terminology, and accessibility cases.
- Ambiguous, incomplete, malformed, oversized, and unsupported requests.
- Correct refusal, caution, escalation, and human-review behavior.
- Direct/indirect prompt injection, jailbreak, data exfiltration, poisoned documents,
  unsafe tool requests, and denial-of-service patterns.
- Privacy leakage, memorization, secrets, employee data, and cross-user/cross-tenant probes.
- Employment fairness, accommodations, protected-group and intersectional slices where
  lawful and necessary.
- Provider timeout, retrieval failure, missing index, stale cache, memory invalidation,
  budget denial, and approved degraded modes.
- Regression cases derived from incidents, complaints, false positives, and false negatives.

Every case records purpose, provenance, license/permission, expected behavior, allowed
answer variants, forbidden behavior, severity, slices, reviewer, and effective dates.
Expected behavior may be an answer, evidence set, refusal, escalation, structured schema,
or explicit unavailable state.

Benchmark examples are not copied blindly from public leaderboards. They must represent the
HRMS use case, supported countries, languages, roles, source quality, and real failure modes.

Every dataset version has `DatasetReviewDate` and `DatasetExpiryDate`. Review confirms that
the benchmark still represents current policies, regulations, languages, populations,
provider/model behavior, attack patterns, and production failures. Configurable warning
events occur before expiry. An expired or overdue dataset cannot support a new promotion or
approval renewal; it must be reviewed and superseded through an immutable version. Expiry
does not delete required historical promotion evidence.

## 5. Separate dataset roles and prevent benchmark contamination

Evaluation data is partitioned into independently versioned roles:

- **Development set:** visible to prompt/retrieval designers for iteration.
- **Validation set:** used to tune thresholds and compare candidates.
- **Sealed holdout set:** restricted and used for formal promotion evidence.
- **Adversarial challenge set:** security and abuse cases, partially restricted.
- **Production incident set:** access-controlled regressions derived from validated incidents.

The sealed holdout is not exposed to prompt authors, routine model tuning, retrieval sources,
or provider training. Access is least-privilege and audited. Case hashes and duplication or
semantic-similarity checks detect leakage between partitions and knowledge indexes.

Synthetic or de-identified data is the default. Real tenant data requires documented
purpose, lawful basis, tenant authorization where required, minimization, encryption,
restricted reviewers/providers, retention/deletion policy, and proof that it is not reused
for another tenant or provider training.

Tenant-specific suites remain in that tenant boundary. A platform benchmark template may
contain only approved synthetic/publicly licensed material and is copied into a tenant-scoped
suite when tenant policy customization is needed. Raw tenant cases and results are never
pooled into a cross-tenant benchmark.

## 6. Store reproducible evaluation evidence in SQL Server

SQL Server is the authoritative evaluation registry and evidence store. Large encrypted
artifacts may use approved object storage with integrity hashes and SQL metadata.

Required conceptual entities:

```text
AI.AiUseCaseRiskProfile
  AiUseCaseRiskProfileId, TenantId, UseCaseKey, RiskClass,
  IntendedPurpose, AffectedPersonTypesJson, DecisionInfluence,
  DataClassificationsJson, JurisdictionsJson, LanguagesJson,
  HumanOversightPolicyVersion, LegalAssessmentReference,
  RiskOwnerRole, RiskOwnerId,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiReleaseCandidate
  AiReleaseCandidateId, TenantId, UseCaseKey, CandidateVersion,
  SystemBundleManifestJson, SystemBundleHash, BaselineCandidateId,
  ChangeClassification, DeploymentScopeJson,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationSuite
  AiEvaluationSuiteId, TenantId, UseCaseKey, RiskProfileVersion,
  Name, Purpose, DatasetPolicyVersion, RequiredSlicesJson,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationDatasetVersion
  AiEvaluationDatasetVersionId, TenantId, AiEvaluationSuiteId,
  DatasetVersion, DatasetRole, ContentHash, ProvenanceJson,
  LicenseAndConsentJson, Classification, CaseCount,
  ContaminationCheckVersion, SealedDate,
  DatasetReviewDate, DatasetExpiryDate,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationCase
  AiEvaluationCaseId, TenantId, AiEvaluationDatasetVersionId,
  CaseKey, CaseFamily, InputArtifactReference,
  ExpectedBehaviorJson, ExpectedEvidenceJson, ForbiddenBehaviorJson,
  Severity, JurisdictionKey, LanguageKey, SliceTagsJson,
  ProvenanceReference, EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationMetricDefinition
  AiEvaluationMetricDefinitionId, TenantId, MetricKey, MetricCategory,
  Definition, Direction, ScaleJson, AggregationPolicyJson,
  EvaluatorType, EvaluatorVersion, UncertaintyMethod,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationGatePolicy
  AiEvaluationGatePolicyId, TenantId, UseCaseKey, RiskClass,
  GateVersion, MandatoryMetricRulesJson, SliceRulesJson,
  CriticalFailureRulesJson, StatisticalPolicyJson,
  ApprovalRolePolicyJson, ApprovalExpiryDays,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationRun
  AiEvaluationRunId, TenantId, AiReleaseCandidateId,
  AiEvaluationSuiteId, DatasetVersionManifestJson,
  EvaluatorVersionManifestJson, ExecutionEnvironmentHash,
  RandomSeedPolicyJson, RepetitionPolicyJson,
  StartedDate, CompletedDate, Status, FailureReason,
  RequestedBy, CorrelationId,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationCaseResult
  AiEvaluationCaseResultId, TenantId, AiEvaluationRunId,
  AiEvaluationCaseId, AttemptNumber, OutputArtifactReference,
  RetrievedEvidenceManifestJson, ToolTraceManifestJson,
  MetricResultsJson, FailureCategoriesJson, Severity,
  HumanReviewRequired, CreatedBy, CreatedDate,
  ModifiedBy, ModifiedDate, IsDeleted, VersionNumber

AI.AiEvaluationHumanReview
  AiEvaluationHumanReviewId, TenantId, AiEvaluationRunId,
  AiEvaluationCaseResultId, ReviewerRole, ReviewerId,
  RubricVersion, BlindReviewGroup, RatingJson,
  DisagreementReason, AdjudicationReference,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiReviewerQualitySnapshot
  AiReviewerQualitySnapshotId, TenantId, ReviewerRole, ReviewerId,
  ReviewPeriodStart, ReviewPeriodEnd, RubricVersion,
  CalibrationSetVersion, ReviewerAgreementScore,
  ReviewerConsistencyScore, ReviewCount, AdjudicationRate,
  QualityStatus, EffectiveFrom, EffectiveTo,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationApproval
  AiEvaluationApprovalId, TenantId, AiReleaseCandidateId,
  AiEvaluationRunId, GatePolicyVersion, Decision,
  DecisionReason, EvidenceManifestHash, ApprovedScopeJson,
  EffectiveFrom, EffectiveTo, ApprovalExpiryReason,
  ApprovedBy, ApprovedDate,
  RevokedBy, RevokedDate,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationDriftSignal
  AiEvaluationDriftSignalId, TenantId, UseCaseKey,
  ProductionCandidateId, SignalType, SliceKey,
  ProviderFingerprintReference, BehaviorBaselineVersion,
  BaselineWindow, ObservationWindow, ObservedValue,
  ThresholdPolicyVersion, Severity, Status,
  DetectedDate, ResolvedDate,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

AI.AiEvaluationIncident
  AiEvaluationIncidentId, TenantId, UseCaseKey,
  ProductionCandidateId, IncidentCategory, Severity,
  EvidenceReference, ContainmentAction, Status,
  OpenedDate, ResolvedDate, RegressionCaseReference,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber

catalog.AiEvaluationSuiteTemplate
  AiEvaluationSuiteTemplateId, UseCaseCategory,
  TemplateVersion, SyntheticArtifactReference, ContentHash,
  EffectiveFrom, EffectiveTo, Status,
  CreatedBy, CreatedDate, ModifiedBy, ModifiedDate,
  IsDeleted, VersionNumber
```

All tenant tables include `TenantId`, SQL Server RLS, tenant-leading indexes, mandatory
audit/version columns, and server-resolved tenant context. The control-plane template cannot
contain tenant, employee, customer, credential, or restricted source content.

Runs, case results, human reviews, and approvals are immutable evidence. Corrections create
linked superseding records; they do not rewrite a prior promotion basis. Evaluation stores
do not retain hidden chain-of-thought.

## 7. Use a provider-independent evaluator architecture

Evaluation executes through stable contracts such as:

- `IEvaluationOrchestrator`
- `IEvaluationDatasetProvider`
- `IRetrievalEvaluator`
- `IGenerationEvaluator`
- `ICitationEvaluator`
- `IConfidenceCalibrationEvaluator`
- `ISecurityEvaluator`
- `IPrivacyEvaluator`
- `IFairnessEvaluator`
- `IToolUseEvaluator`
- `IHumanReviewCoordinator`
- `IEvaluationGateEvaluator`

Deterministic and self-hosted evaluators are preferred where they provide reliable evidence.
RAGAS or other libraries may be used behind adapters for selected metrics, but no library,
provider dashboard, or paid evaluation service becomes the architecture or the system of
record.

Provider-specific evaluation output is normalized to platform metric definitions while raw
diagnostic metadata is retained in a versioned, access-controlled extension object. Adding
or replacing an evaluator requires adapter/configuration changes, not AI feature-code
changes.

## 8. Measure multiple dimensions without hiding critical failures

Each use case selects metrics from this minimum taxonomy:

| Category | Required enterprise measures where applicable |
|---|---|
| Retrieval | Recall@K, Precision@K, nDCG@K, MRR, authorized-hit rate, no-result correctness, source diversity, duplication, effective-date and jurisdiction correctness |
| Grounding | Claim-level evidence support, faithfulness, unsupported-claim rate, `HallucinationRate`, `HallucinationSeverity`, contradiction handling |
| Citations | Citation precision, recall, completeness, source identity/version integrity, quoted-span support |
| Answer quality | Correctness, completeness, relevance, usefulness, instruction and schema adherence |
| Refusal/escalation | Correct refusal, false refusal, unsafe compliance, insufficient-evidence behavior, human escalation |
| Confidence | Calibration error, Brier score where applicable, reliability by band/slice, selective risk and coverage |
| Security/privacy | Attack success, leakage, unauthorized retrieval/tool use, poisoned-context resistance, secret/PII exposure |
| Fairness/human impact | Error and outcome differences by approved groups/slices, accessibility, accommodation and oversight effectiveness |
| Memory/cache | Summary faithfulness/lineage, stale-authority rejection, purpose isolation, cache correctness and invalidation |
| Operations | p50/p95/p99 latency, availability, timeout/fallback, tokens, cost, concurrency and degraded-mode correctness |

Metric names alone are insufficient. Every metric definition states unit, direction,
population, aggregation, minimum sample policy, uncertainty method, slices, evaluator,
known limitations, and what decision it may influence.

Composite scores may be displayed for trend reporting but cannot override a failed mandatory
gate or critical case. Tenant-isolation, authorization, severe data leakage, prohibited
employment action, and other critical failures are evaluated independently.

`HallucinationRate` is the proportion of evaluated material claims classified as fabricated,
unsupported, contradicted, or incorrectly attributed under the approved metric definition.
`HallucinationSeverity` records the highest and distribution of harm severity, including
whether a claim affects payroll, policy, compliance, employment rights, safety, privacy, or
authorization. A low rate cannot offset one critical hallucination. Claim materiality,
severity taxonomy, evaluator versions, uncertainty, and aggregation are effective-dated and
auditable.

## 9. Evaluate retrieval before evaluating the final answer

Retrieval evaluation uses authorized expected evidence, not only textual similarity. It
verifies:

- The correct tenant, user permission, purpose, delegation, and data-classification scope.
- Source approval state, jurisdiction, language, effective date, and supersession state.
- Whether relevant evidence appears within configured `K` and irrelevant evidence is excluded.
- Ranking quality and source diversity without duplicate chunks dominating context.
- Correct no-result behavior when no authorized/current evidence exists.
- Resistance to poisoned documents and instructions embedded in retrieved text.
- Stable normalized behavior across Qdrant and future `IVectorStore` adapters.

Vector similarity scores are provider diagnostics, not universal quality probabilities.
Retrieval gates are calibrated per use case, corpus, language, and adapter. A final answer
cannot compensate for cross-tenant or unauthorized retrieval.

## 10. Evaluate generation and citations at claim level

Generation evaluation separates:

- Whether the response follows system, tenant, use-case, and output-schema instructions.
- Whether each material factual/policy/payroll claim is supported by authorized evidence.
- Whether cited sources actually support the associated claim and use the correct version.
- Whether the response handles conflicts, missing evidence, uncertainty, and effective dates.
- Whether it avoids invented policy, payroll figures, legal certainty, or unsupported action.
- Whether tone, language, readability, accessibility, and requested format are appropriate.

Citation completeness uses the approved policy benchmark baseline in AI Strategy v2.1 and
the effective gate policy. A high citation count does not pass evaluation when citations are
irrelevant, stale, unauthorized, or do not support the claims.

Payroll, compliance, and employment guidance requires domain-expert review of material
claims. A fluent answer cannot offset a critical factual or legal error.

## 11. Calibrate confidence, refusal, and escalation behavior

The `confidenceScore` and bands from ADR-019 are calibrated against approved labeled cases.
Evaluation measures whether confidence corresponds to supported correctness and whether
lower-confidence cases are safely refused or escalated.

Required evidence includes:

- Reliability by confidence band and important slice.
- Calibration error and Brier score where the label supports probabilistic evaluation.
- Selective risk at different coverage/abstention levels.
- False-high-confidence and false-low-confidence rates.
- Correct treatment of missing, conflicting, stale, or unauthorized evidence.
- Stability after model, prompt, index, provider, language, or policy changes.

Thresholds and weights are effective-dated configuration. They are not universal truth and
cannot grant authorization. Critical conflict or unsupported policy/payroll claims must
refuse/escalate regardless of an aggregate confidence score.

`SummaryQualityScore` from ADR-032 is evaluated against summary faithfulness, source-turn
coverage, omission, authorization, and regeneration benchmarks. It remains informational
and cannot elevate source trust or authorization.

## 12. Maintain a mandatory security and privacy evaluation suite

Security evaluation is mapped to the current approved security threat model and OWASP GenAI
risks. It includes:

- Direct and indirect prompt injection, system-prompt extraction, and jailbreaks.
- Sensitive-information disclosure, memorization probes, and cross-tenant/user extraction.
- Poisoned knowledge, malicious metadata, corrupted files, and retrieval manipulation.
- Unsafe output handling, tool-parameter injection, IDOR, excessive agency, and privilege
  escalation.
- Model/provider denial of service, oversized context, cost amplification, and retry abuse.
- Supply-chain and provider/adapter version change scenarios.
- Insecure fallback, cache probing, stale memory, and permission-change races.
- Misinformation and overconfident unsupported employment/payroll/policy conclusions.

Critical tenant-isolation and authorization cases require zero unauthorized disclosure or
action. A detected critical failure blocks promotion, triggers incident handling, and cannot
be waived by a composite score, cost override, product deadline, or model-as-judge result.

Evaluation artifacts themselves are treated as attackable sensitive assets. Inputs and
retrieved documents remain untrusted data; evaluator prompts cannot authorize tools or
override platform policy.

## 13. Apply employment fairness, accessibility, and human-impact evaluation

High-impact employment decision-support use cases require a documented legal/fairness plan
before evaluation. The plan defines affected groups, lawful use of sensitive attributes,
job-related criteria, jurisdictions, accommodations, expected human role, appeal/contest
process, and prohibited proxy features.

Where lawful and statistically meaningful, evaluation examines:

- Error, false-positive, false-negative, abstention, and escalation rates by group.
- Selection or recommendation-rate differences under the applicable legal method.
- Calibration and ranking quality by group and intersectional slice.
- Language, disability/accessibility, location, age, gender, and other protected or
  vulnerable-group impacts relevant to the jurisdiction and use case.
- Whether a human reviewer can understand evidence, disagree, correct, and record reasons.
- Whether users over-rely on AI recommendations or rubber-stamp outputs.

No single fairness metric is assumed to prove fairness. Metrics and acceptable analysis are
approved by legal, privacy, HR domain, and fairness reviewers for the specific use case.
Small-group reporting uses privacy-preserving minimum-count and suppression policies.
Protected attributes are not sent to an LLM provider unless separately lawful, necessary,
approved, and contractually protected.

An aggregate quality improvement cannot offset a material regression for an affected group.
Production experiments that vary employment recommendations across groups are prohibited.

## 14. Evaluate supported languages, locales, and accessibility independently

Every production-supported language/locale is a mandatory evaluation slice, not a sample
translation of the English benchmark. Native or qualified reviewers validate terminology,
policy meaning, dates, numbers, currency, names, honorifics, and culturally/contextually
appropriate escalation.

The platform measures cross-language retrieval, citation support, refusal, safety, confidence
calibration, and latency/cost. Unsupported languages produce a clear safe response or route
to an approved supported language; they do not silently receive a lower-quality translation.

Evaluation UIs and human-review workflows follow the approved accessibility standard and do
not communicate pass/fail, confidence, or severity by color alone.

## 15. Combine deterministic, model-graded, and human evaluation

Evaluator precedence is:

1. Deterministic controls for authorization, schema, source identity/version, citation links,
   prohibited content, exact calculations, and invariant business/security rules.
2. Statistical/semantic evaluators for retrieval, similarity, calibration, drift, and
   well-defined quality dimensions.
3. Model-as-judge for rubric-based assistance where deterministic grading is insufficient.
4. Qualified human review for domain correctness, material harm, fairness, legal/compliance,
   localization, and promotion accountability.

Model-as-judge is never the sole approval signal. Each judge is versioned and calibrated
against a sealed human-labeled set. The process measures disagreement, position/order bias,
verbosity/style bias, self-provider preference, and stability across repeated runs. Candidate
identity/provider is hidden where practical, pair order is randomized, and judge rationale
is treated as diagnostic output rather than hidden authority.

Sensitive cases cannot be sent to an external judge provider without approved processing,
residency, retention, contract, and tenant policy. A candidate model does not approve itself.

Human review uses versioned rubrics, blinded sampling where possible, role qualification,
conflict-of-interest controls, and adjudication. Inter-rater agreement is measured; material
disagreement is resolved rather than averaged away.

`ReviewerAgreementScore` measures alignment with peer/adjudicated outcomes under the same
rubric and comparable case population. `ReviewerConsistencyScore` measures stability on
calibration or repeated equivalent cases over time. Both are versioned, uncertainty-aware
governance signals, not employee-performance decisions. They identify rubric ambiguity,
reviewer training needs, adjudication drift, or insufficient review volume. Low or
statistically insufficient scores trigger calibration/training or restricted review scope;
they cannot silently discard an unfavorable expert review.

## 16. Require statistical rigor and reproducibility

Formal evaluation reports include:

- Candidate and baseline sample counts by metric and slice.
- Point estimate, uncertainty/confidence interval, and approved statistical method.
- Paired comparison where the same cases are used.
- Non-inferiority or regression tolerance defined before the run.
- Tail and worst-slice results, not averages alone.
- Repeated trials for nondeterministic outputs under a versioned repetition policy.
- Provider/model parameters, environment hash, time, seed policy, and dependency versions.
- Missing, invalid, timed-out, or unscorable cases; these cannot silently disappear.

Sample size is based on risk, expected effect, base rate, variability, slices, and desired
decision confidence. It is not a fixed classroom-sized number. Small samples are labeled
insufficient and cannot support a formal high-impact promotion.

Temperature and other stochastic settings are pinned where supported. When a provider does
not guarantee determinism, evaluation reports output distributions and stability rather
than claiming exact reproducibility.

## 17. Enforce independent promotion gates and segregation of duties

Release-candidate states are:

`Draft -> Sandbox -> Evaluating -> Review -> ApprovedForCanary -> Canary -> Production`

Terminal/control states include `Blocked`, `Suspended`, `RolledBack`, and `Retired`.

A production promotion requires one immutable evidence bundle containing:

- Approved risk profile, evaluation suite, data versions, and gate policy.
- Candidate-versus-current-baseline report with uncertainty and slice results.
- Security/privacy and tenant-isolation evidence.
- Domain and human-review evidence.
- Fairness/legal/accessibility evidence for high-impact use cases.
- Latency, cost, capacity, fallback, and degraded-mode evidence.
- Known limitations, residual risks, monitoring plan, rollback version, and approval expiry.

The candidate owner cannot be the sole approver. Required approvals are effective-dated by
risk class and include Product/AI owner, domain owner, security/privacy, operations, and for
high-impact use cases legal/fairness and accountable HR leadership.

Mandatory hard blocks include:

- Any cross-tenant or unauthorized data/tool access.
- Critical sensitive-data disclosure or security-control bypass.
- Prohibited autonomous employment action.
- Unsupported definitive payroll, policy, compliance, or employment claim classified as
  critical by the gate policy.
- Benchmark integrity, contamination, missing lineage, or evidence-tampering failure.
- Failure of required human, legal, privacy, security, or fairness approval.

Quality, safety, security, fairness, latency, and cost are separate gates. A saving under
ADR-033 cannot buy down a safety failure, and an emergency cost override cannot bypass an
evaluation gate.

## 18. Classify changes and trigger proportionate re-evaluation

Every change receives one of these effective-dated classifications:

- **Editorial:** no semantic/runtime effect, supported by deterministic proof.
- **Low-risk configuration delta:** narrow impact with approved targeted regression.
- **Material:** model, prompt meaning, retrieval, tool, safety, confidence, memory, cache,
  provider behavior, knowledge policy, or affected population change.
- **Critical:** authorization, tenant isolation, employment decision influence, sensitive
  data, legal obligation, or incident remediation change.

Material and critical changes require a new release candidate and the full applicable suite.
Targeted evaluation is allowed only when dependency/impact analysis proves unaffected gates
and the gate policy permits it. Unknown impact defaults to broader evaluation.

Revalidation is triggered by:

- Model/provider alias, fingerprint, terms, safety behavior, or adapter change.
- Prompt, tool, embedding, chunking, reranking, index, source-policy, confidence, memory,
  cache, budget-routing, guardrail, or evaluator change.
- New language, country, tenant policy, role, data class, or affected population.
- Permission matrix, effective-dating, regulation, legal interpretation, or HR policy change.
- Quality/security/privacy/fairness incident, drift alert, complaint, or material user harm.
- Dataset review/expiry, provider behavior drift, or risk-owner/accountability change.
- Approval expiry or scheduled risk-based review.

Changing only the evaluator requires re-baselining the current production candidate before
the new evaluator can compare a release candidate.

## 19. Use shadow and canary stages without experimenting on employment rights

After offline approval, eligible candidates may progress through:

1. Sandbox using synthetic/de-identified data.
2. Shadow comparison with no user-visible or decision influence, only when production-data
   processing is approved.
3. Limited canary by approved tenant/use case/role scope.
4. Phased production expansion with monitored gates.

Shadow/canary assignment is tenant-safe, audited, reversible, and excluded from unauthorized
populations. Users are informed where required. High-impact employment outputs cannot be
randomly varied as an uncontrolled A/B experiment. Any controlled study involving affected
people requires separate legal, ethics/privacy, and Product Owner approval.

Canary stop conditions are configured before activation and include critical incidents,
quality/slice regression, abnormal refusal, cost/latency breach, security signal, and human
review failure. Promotion does not proceed while required evidence is delayed or unavailable.

## 20. Monitor production quality and drift as post-deployment evaluation

ADR-031 telemetry and the evaluation service monitor:

- Input/topic/language/role distribution drift.
- Retrieval hit/no-result, rank, source diversity, freshness, and authorization rejection.
- Groundedness, citation support, confidence distribution/calibration, refusals, and
  escalations.
- Security/privacy detections, attacks, leakage, and abnormal tool behavior.
- Human corrections, complaints, appeals, incidents, and confirmed business outcomes.
- Group/slice outcomes for approved high-impact monitoring.
- Latency, token, cost, provider, cache, memory, fallback, and degraded mode.
- Knowledge, permission, source, and model/provider version changes.

`ProviderBehaviorDrift` is a first-class `SignalType` classification for a statistically or
operationally material behavior change from an externally managed provider/model even when
the advertised model name or configured alias is unchanged. Detection uses versioned
sentinel suites, repeated baseline cases, provider fingerprint/metadata where available,
output/refusal/safety/tool/citation distributions, and incident signals. Material provider
behavior drift freezes promotion and triggers scoped suspension or revalidation according to
severity; prior approval is not inherited automatically.

User thumbs-up/down and free-text feedback are signals, not ground truth. Feedback is checked
for abuse, sampling bias, duplicates, authorization, and privacy before it influences a
benchmark or promotion decision.

Online quality sampling is risk-based and privacy-minimized. Prompts/responses are not copied
into general telemetry. Content review requires approved sampling policy, restricted storage,
encryption, retention, reviewer access, and tenant/employee privacy controls.

Each drift signal has an effective-dated threshold, severity, owner, response time, and
action: observe, targeted evaluation, freeze promotion, reduce scope, disable feature,
rollback, or incident response.

## 21. Convert validated incidents into regression evidence

Quality, security, privacy, fairness, and domain incidents follow an auditable lifecycle:

1. Detect and classify severity.
2. Contain exposure and preserve restricted evidence.
3. Suspend/rollback affected scope when required.
4. Determine root cause across the full system bundle.
5. Create a minimized regression case and update the relevant challenge suite.
6. Evaluate the fix and current baseline.
7. Obtain independent approval before reactivation.
8. Monitor post-fix effectiveness and close through post-incident review.

The regression case must not unnecessarily retain employee or tenant content. Where the
original content cannot be retained, an authorized synthetic equivalent and protected
incident reference preserve the failure semantics.

## 22. Define deterministic rollback and approval expiry

Every production release retains a tested rollback candidate and deployment manifest.
Rollback must restore compatible prompt/model/index/policy/cache/memory bindings, not only
change the model name.

Critical tenant isolation, data leakage, unsafe employment action, or security failure
triggers immediate containment and rollback/disablement under the incident runbook. Other
regressions follow the severity and error-budget policy in ADR-031.

Evaluation approval expires after the effective-dated period set by risk policy. Expiry does
not silently renew. Production may continue only under an approved renewal/revalidation or a
separately documented, time-bound operational exception that cannot waive critical security,
tenant, privacy, legal, or prohibited-use controls.

Every approval records `ApprovalExpiryReason`, selected from an effective-dated governance
catalog with an optional bounded supporting reference. Initial reason classes include
scheduled review cycle, dataset expiry, policy/regulatory change, incident revalidation,
provider/model change, provider behavior drift, risk-profile change, and manual revocation.
The reason is included in expiry warnings, events, APIs, audit, and operational review; it
cannot contain unnecessary employee or tenant content.

## 23. Control evaluation cost without weakening evidence

ADR-033 budgets evaluation by tenant, use case, candidate, suite, evaluator, provider, and
environment. Cost controls may:

- Run deterministic checks before model-graded or human review.
- Use stratified sampling for low-risk online monitoring.
- Reuse immutable results only when the candidate bundle and evidence remain identical.
- Route to a lower-cost judge only after that judge is independently calibrated and approved.
- Schedule non-urgent large suites within approved capacity windows.

Budget exhaustion blocks promotion rather than silently reducing mandatory cases, slices,
repetitions, reviewers, or security tests. No paid evaluation service is required for initial
development. Self-hosted/deterministic evaluators and approved local models may be used where
they satisfy the same evidence requirements.

## 24. Define versioned API and permission requirements

The Phase 6D OpenAPI package must include:

| Endpoint | Permission | Behavior |
|---|---|---|
| `GET /api/v1/ai/admin/evaluation-suites` | `AI.ViewEvaluations` | Tenant-scoped suite/version metadata and readiness |
| `POST /api/v1/ai/admin/evaluation-suites` | `AI.ManageEvaluations` | Create Draft suite from approved template or tenant design |
| `POST /api/v1/ai/admin/evaluation-suites/{id}/versions` | `AI.ManageEvaluations` | Create immutable effective-dated suite/dataset version |
| `POST /api/v1/ai/admin/evaluation-runs` | `AI.RunEvaluations` | Start idempotent run for an immutable candidate and suite |
| `GET /api/v1/ai/admin/evaluation-runs/{id}` | `AI.ViewEvaluations` | Results, uncertainty, slices, failures, evidence, and gate status |
| `POST /api/v1/ai/admin/evaluation-runs/{id}/human-reviews` | `AI.ReviewEvaluations` | Submit rubric-versioned review without overwriting prior review |
| `POST /api/v1/ai/admin/release-candidates` | `AI.ManageModels` | Register immutable system bundle and baseline |
| `GET /api/v1/ai/admin/release-candidates/{id}/evidence` | `AI.ViewEvaluations` | Return authorized evidence manifest, limitations, and approvals |
| `POST /api/v1/ai/admin/release-candidates/{id}/approve-canary` | `AI.ApproveAiPromotion` | Record independent scoped approval after all gates pass |
| `POST /api/v1/ai/admin/release-candidates/{id}/promote` | `AI.PromoteAiRelease` | Promote approved canary/production scope with concurrency control |
| `POST /api/v1/ai/admin/release-candidates/{id}/rollback` | `AI.RollbackAiRelease` | Roll back/disable scope with reason, incident, and immutable audit |
| `GET /api/v1/ai/admin/evaluation-drift` | `AI.ViewEvaluations` | Tenant-scoped signals, including provider behavior drift, severity, thresholds, and revalidation state |

Evaluation-suite/dataset responses expose review/expiry state; result responses expose
`HallucinationRate`, `HallucinationSeverity`, and reviewer-quality metric versions; approval
responses expose `ApprovalExpiryReason`; drift responses identify
`ProviderBehaviorDrift` explicitly. Sensitive reviewer identity remains role/ABAC protected.

All endpoints use `/api/v1`, JWT, server-resolved tenant context, RBAC plus ABAC, correlation
IDs, standard envelopes, pagination/filter limits, audit, and rate limits. Mutations require
`Idempotency-Key` and optimistic concurrency. Dataset/artifact upload uses approved malware,
content-type, size, classification, encryption, and retention controls.

Initial permissions:

| Permission | Scope |
|---|---|
| `AI.ViewEvaluations` | View authorized tenant evaluation metadata/results |
| `AI.ManageEvaluations` | Create effective-dated suite, dataset, metric, and gate-policy versions |
| `AI.RunEvaluations` | Execute approved tenant-scoped suites and candidates |
| `AI.ReviewEvaluations` | Submit qualified rubric-based human review |
| `AI.ApproveAiPromotion` | Independently approve candidate scope after gates pass |
| `AI.PromoteAiRelease` | Activate only an approved candidate/scope |
| `AI.RollbackAiRelease` | Immediately reduce scope, disable, or roll back with audit |
| `AI.ViewAllEvaluationHealth` | Restricted platform cross-tenant aggregate health without tenant content |

Suite author, candidate owner, human reviewer, approver, and promoter duties are separated by
risk policy. Support impersonation cannot grant evaluation or promotion permissions.

## 25. Publish evaluation events through the outbox

ADR-009 events include:

- `AiEvaluationSuiteVersionCreated`
- `AiEvaluationRunStarted`
- `AiEvaluationRunCompleted`
- `AiEvaluationGateFailed`
- `AiHumanReviewRequired`
- `AiReleaseCandidateApprovedForCanary`
- `AiReleaseCandidatePromoted`
- `AiReleaseCandidateSuspended`
- `AiReleaseCandidateRolledBack`
- `AiEvaluationApprovalExpiring`
- `AiEvaluationApprovalExpired`
- `AiEvaluationDatasetReviewDue`
- `AiEvaluationDatasetExpired`
- `AiProviderBehaviorDriftDetected`
- `AiReviewerQualityDegraded`
- `AiQualityDriftDetected`
- `AiEvaluationRevalidationRequired`
- `AiEvaluationIncidentOpened`
- `AiEvaluationIncidentResolved`

Events contain identifiers, versions, scope, status, severity, and correlation data only.
They do not contain prompts, responses, employee data, benchmark answers, credentials,
protected attributes, or judge rationale. Consumers are idempotent.

## 26. Observe the evaluation system without exposing content

ADR-031 telemetry includes low-cardinality measures for:

- Run queue time, duration, completion, failure, timeout, and cancellation.
- Case counts, valid/unscorable rate, evaluator failures, and human-review backlog.
- Gate pass/fail by metric category, risk class, language, and environment.
- Candidate-versus-baseline regression and worst-slice status.
- Judge/human disagreement, inter-rater agreement, and calibration drift.
- Reviewer agreement/consistency score distributions, insufficient-sample state, training/
  adjudication backlog, and quality degradation by approved reviewer role.
- Hallucination rate and severity distribution by use case, risk class, language,
  jurisdiction, candidate, and approved low-cardinality slice.
- Dataset review age, expiry warnings/overdue state, and blocked-run/promotion count.
- Provider behavior drift count, severity, affected candidate/scope, and revalidation state.
- Approval age/expiry, canary state, rollback, incident, and revalidation backlog.
- Production quality/drift signal count, severity, age, and response state.
- Evaluation tokens, cost, provider errors, and capacity.

Tenant ID, user/employee ID, prompts, answers, retrieved text, case answers, protected-group
attributes, and unrestricted case keys are prohibited as general metrics/log labels. Detailed
drilldown uses authorized evaluation APIs and evidence storage.

## 27. Fail closed for promotion and safely for current production

- Missing, stale, incomplete, contaminated, or unverifiable evidence is not a pass.
- An expired/overdue dataset or missing accountable risk owner cannot support promotion or
  approval renewal.
- Evaluation-service, dataset, evaluator, authorization, or evidence-store failure blocks
  new promotion and approval renewal.
- A model-as-judge outage cannot be replaced by an unapproved judge or skipped silently.
- Missing required human/legal/security/privacy/fairness approval blocks promotion.
- Unknown provider model/fingerprint change suspends new traffic or routes to the last
  approved candidate according to policy; it does not inherit prior approval automatically.
- Material `ProviderBehaviorDrift` is treated as a change even when the provider model name
  is unchanged.
- Critical production safety, tenant, security, privacy, or prohibited-use failure triggers
  containment and rollback/disablement.
- Non-critical evaluation outage does not automatically stop a healthy current production
  candidate before its approval expires, but freezes promotion and increases monitoring.
- Rollback failure triggers feature disablement or approved retrieval-only/manual fallback.
- Core HRMS functionality remains available without AI.

## 28. Apply retention, privacy, legal hold, and deletion controls

ADR-022 must finalize retention for suites, artifacts, runs, reviews, approvals, drift, and
incidents before implementation approval. Retention is effective-dated by classification,
risk, legal/financial/security need, and tenant policy.

Evaluation evidence stores the minimum content needed to reproduce and audit the decision.
Sensitive artifacts are encrypted with restricted access, download controls, watermarking
where appropriate, and immutable access logs. Legal hold does not make held evaluation data
available to AI generation or unrelated reviewers.

Eligible deletion covers tenant cases, generated outputs, provider-side temporary state,
object-store artifacts, derived embeddings/caches, exports, replicas, and backups under the
approved deletion process. Mandatory audit/evidence retention is separated from reusable AI
content.

Dataset expiry retires a dataset from future promotion evidence but does not erase historical
runs, approvals, expiry reasons, or legal/security records that remain within retention.
Reviewer quality snapshots use minimized reviewer references and restricted access; they are
not repurposed for unrelated HR performance management.

## 29. Deliver evaluation capability in controlled increments

Implementation documentation must preserve this order:

1. Risk profiles, release-bundle manifest, suite/dataset governance, deterministic metrics,
   tenant isolation, and immutable evidence.
2. Retrieval, generation, citation, confidence, refusal, security, and privacy evaluation.
3. Human/domain review, statistical comparison, promotion, canary, and rollback gates.
4. Employment fairness, accessibility, legal/human-oversight evidence for high-impact use.
5. Production sampling, drift, incident learning, approval expiry, and revalidation.
6. Optional provider/library evaluators only after adapter and calibration approval.

No later increment may bypass an earlier control. No AI evaluation code starts until the
constitutional Business, Technical, Database, UI, and Test documents plus Security and
OpenAPI requirements are Approved.

---

# Alternatives Considered

## Approve using vendor benchmarks or model leaderboards

Vendor/public benchmarks do not represent tenant authorization, HR domain rules, effective
dates, supported languages, proprietary sources, tools, or affected employee populations.
Rejected as production evidence.

## Evaluate only the language model

Misses prompt, retrieval, index, source, tool, guardrail, memory, cache, and provider-adapter
failures. Rejected in favor of immutable full-system release candidates.

## Use model-as-judge as the sole evaluator

Scales well but introduces judge bias, instability, self-preference, data-processing, and
explainability risks. Rejected as the sole approval signal.

## Use only human review

Provides domain nuance but is slow, expensive, variable, and insufficient for broad security,
regression, concurrency, and retrieval coverage. Rejected as the sole method.

## Use one global benchmark and threshold for every tenant/use case

Ignores purpose, language, country, role, policy, risk, and corpus differences and can leak
tenant data. Rejected.

## Allow production promotion on improved average quality

Averages can hide critical security, minority-slice, language, refusal, and payroll/policy
failures. Rejected in favor of independent hard gates and worst-slice review.

## Evaluate once before first release

Provider, model, source, permission, regulation, behavior, and population drift make a
one-time approval stale. Rejected in favor of monitored approval expiry and revalidation.

## Require a paid managed evaluation platform first

Could accelerate tooling but creates initial cost and vendor dependency. Rejected as a
mandatory first choice. Optional services may integrate through provider-neutral adapters.

---

# Consequences

## Positive

- Production approval is tied to a reproducible full-system bundle and evidence hash.
- Tenant isolation, security, and prohibited employment actions cannot be averaged away.
- Retrieval, generation, citations, confidence, fairness, cost, and operations are evaluated
  together but remain independent gates.
- Provider/model/evaluator changes remain plug-in and configuration driven.
- Domain experts and accountable human approvers remain part of high-impact decisions.
- Drift, incidents, approval expiry, and rollback create continuous assurance.
- Initial development can use self-hosted and deterministic evaluators without paid services.

## Negative

- Enterprise benchmark curation, sealed holdouts, human review, and fairness analysis require
  sustained domain and governance effort.
- Formal evaluation increases release lead time and operating cost.
- Provider nondeterminism limits exact reproducibility.
- Small slices and rare harms can require long observation periods or targeted data creation.
- Strict fail-closed promotion may delay beneficial model or prompt upgrades.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Benchmark overfitting/contamination | Partitioned data roles, sealed holdout, hashes, similarity checks, access audit |
| Model judge bias or self-preference | Calibrate to human labels, blind identity, randomize order, version judge, never sole gate |
| Average score hides harmful slice | Mandatory slice rules, worst-slice reporting, hard blocks, legal/domain review |
| Cross-tenant evaluation disclosure | Tenant RLS, tenant-scoped artifacts, synthetic global templates, negative tests |
| Provider silently changes model | Pin version/fingerprint, detect change, suspend/revalidate, approved fallback |
| Human review is inconsistent | Versioned rubric, qualification, blinding, agreement metric, adjudication |
| Hallucination trend is hidden by aggregate quality | Explicit rate and severity metrics; critical claims remain hard blocks |
| Dataset becomes stale or overfitted | Review/expiry dates, warnings, rotation, sealed holdout, superseding versions |
| Approval expiry lacks accountability | Governed expiry-reason catalog, API/event/audit visibility, no silent renewal |
| Risk ownership becomes ambiguous | Effective-dated accountable role/principal and escalation on missing owner |
| Reviewer quality degrades | Agreement/consistency monitoring, minimum evidence, calibration, training, adjudication |
| Provider behavior changes without rename | Sentinel suites, explicit drift classification, freeze/suspend and revalidation |
| Production drift after approval | Online signals, approval expiry, sentinel/incident suites, revalidation triggers |
| Evaluation cost causes skipped evidence | ADR-033 budgets; deterministic-first execution; budget denial blocks promotion |
| Protected attributes create privacy risk | Lawful-purpose review, minimization, restricted enclave, suppression, no provider transfer by default |
| Rollback restores incompatible parts | Full bundle manifest, compatibility checks, rehearsed rollback/disablement |
| User feedback becomes false ground truth | Abuse/bias validation, expert confirmation, controlled benchmark admission |
| Evaluator/library lock-in | Provider-neutral contracts, normalized metrics, immutable platform evidence |

---

# Acceptance Criteria Before Approval/Implementation

| ID | Criterion |
|---|---|
| EV-AC-001 | Every AI use case has an effective-dated risk profile, intended purpose, affected-person analysis, jurisdictions, data classes, human-oversight policy, and accountable owner. |
| EV-AC-002 | Autonomous/state-changing hiring, firing, promotion, compensation, discipline, or other employment decisions remain prohibited without a separate Approved architecture and full documentation set. |
| EV-AC-003 | Every evaluation and production promotion binds an immutable full-system release-candidate manifest and hash, not only a model name. |
| EV-AC-004 | Suites cover applicable domain, retrieval, citation, confidence, refusal, tenant/permission, effective-date, multilingual, security, privacy, fairness, accessibility, cost, latency, and failure-mode cases. |
| EV-AC-005 | Development, validation, sealed holdout, adversarial, and incident sets have separate version, access, provenance, contamination, retention, and audit controls. |
| EV-AC-006 | Real tenant evaluation data is prohibited by default and, when approved, remains minimized, encrypted, purpose-bound, tenant-isolated, retention-controlled, and excluded from provider training. |
| EV-AC-007 | Cross-tenant, cross-user, guessed-ID, delegation, permission-change, and purpose-boundary cases produce zero unauthorized retrieval, output, tool access, memory, cache, or evidence disclosure. |
| EV-AC-008 | Retrieval reports Recall@K/Precision@K/nDCG/MRR where labeled data permits, plus authorization, jurisdiction, effective-date, no-result, diversity, and poison-resistance results. |
| EV-AC-009 | Claim-level grounding and citation evaluation proves material policy/payroll claims use current authorized supporting sources or safely refuse/escalate. |
| EV-AC-010 | Confidence and bands are calibrated by use case and important slice; critical conflict or unsupported claims cannot pass through aggregate confidence. |
| EV-AC-011 | Direct/indirect injection, jailbreak, exfiltration, poisoned source, unsafe tool, excessive-agency, denial-of-service, fallback, and misinformation suites pass all mandatory security gates. |
| EV-AC-012 | High-impact employment decision support has Approved legal/fairness/privacy/accessibility analysis, qualified human review, appeal/contest design, and meaningful oversight evidence. |
| EV-AC-013 | Aggregate improvement cannot approve a material regression for a required language, jurisdiction, role, affected group, or other mandatory slice. |
| EV-AC-014 | Every supported language/locale has independent retrieval, grounding, citation, refusal, safety, confidence, and domain review evidence. |
| EV-AC-015 | Model-as-judge is versioned, blinded where practical, bias/stability tested, calibrated to human labels, and never the sole approval signal. |
| EV-AC-016 | Human review records rubric version, reviewer qualification, conflicts, blind group, agreement/disagreement, adjudication, and immutable audit. |
| EV-AC-017 | Formal reports include sample/slice counts, uncertainty, paired baseline comparison, predeclared tolerance, repeated-run policy, environment hash, and all invalid/unscorable cases. |
| EV-AC-018 | Promotion is blocked on missing/stale/unverifiable evidence, mandatory gate failure, benchmark-integrity failure, or missing required independent approval. |
| EV-AC-019 | Candidate owner cannot be sole approver; role separation is enforced for suite authoring, review, approval, promotion, and rollback according to risk class. |
| EV-AC-020 | Shadow/canary deployment is scoped, tenant-safe, reversible, monitored, and cannot run uncontrolled employment experiments or influence decisions before approval. |
| EV-AC-021 | Material/critical component, provider, population, policy, permission, regulation, language, or evaluator changes trigger the approved re-evaluation scope. |
| EV-AC-022 | Production drift monitors quality, retrieval, confidence, security, privacy, feedback, group/slice, cost, latency, cache, memory, and version signals without placing sensitive content in telemetry. |
| EV-AC-023 | Critical production failure triggers containment and tested full-bundle rollback/disablement; rollback failure reaches an approved manual/retrieval-only fallback. |
| EV-AC-024 | Validated incidents generate minimized regression cases, root-cause lineage, re-evaluation evidence, independent reactivation approval, and post-fix monitoring. |
| EV-AC-025 | Evaluation approval is effective-dated and expires; renewal requires current evidence and cannot silently inherit approval after provider/model/fingerprint change. |
| EV-AC-026 | Evaluation budget exhaustion cannot reduce mandatory cases, slices, repetitions, reviewers, or security/fairness evidence and blocks promotion instead. |
| EV-AC-027 | Evaluator/provider/library replacement uses adapters/configuration and requires no AI feature-code change or loss of historical result reproducibility. |
| EV-AC-028 | Evaluation APIs are versioned, OpenAPI-documented, tenant-isolated, RBAC/ABAC protected, idempotent where mutable, audited, rate-limited, and contract-tested. |
| EV-AC-029 | Evaluation events use the transactional outbox, are idempotent, and contain no prompts, answers, employee data, protected attributes, credentials, or benchmark answers. |
| EV-AC-030 | Retention, deletion, legal hold, provider-state deletion, artifact integrity, and access logging satisfy Approved ADR-022 and privacy/security designs. |
| EV-AC-031 | Evaluation-service failure blocks promotion but does not silently replace evaluators, skip evidence, or misclassify a missing result as pass. |
| EV-AC-032 | Unit coverage is at least 85%, with integration, statistical, isolation, security, privacy, fairness, concurrency, failover, drift, promotion, rollback, and end-to-end tests. |
| EV-AC-033 | Reports expose effective-dated `HallucinationRate` and `HallucinationSeverity`; a low aggregate rate cannot offset a critical hallucination. |
| EV-AC-034 | Every risk profile has an effective-dated accountable `RiskOwnerRole` and `RiskOwnerId`; missing ownership blocks promotion/renewal and ownership changes preserve history. |
| EV-AC-035 | Every dataset version has `DatasetReviewDate` and `DatasetExpiryDate`, generates review/expiry warnings, and cannot support new promotion/renewal after expiry until superseded. |
| EV-AC-036 | Every approval expiry records a governed `ApprovalExpiryReason` visible in authorized APIs, events, audit, and operational review without sensitive free text. |
| EV-AC-037 | `ProviderBehaviorDrift` is detected independently of model-name changes and triggers severity-based promotion freeze, suspension, or revalidation. |
| EV-AC-038 | Human review quality records versioned `ReviewerAgreementScore` and `ReviewerConsistencyScore`, uncertainty/sample sufficiency, calibration action, and adjudication without repurposing the data for unrelated HR performance management. |

---

# Impact

## Architecture

Adds a provider-independent AI Evaluation Service, use-case risk registry, immutable release
candidate manifests, governed datasets/evaluators, promotion workflow, online drift service,
incident-to-regression flow, dataset rotation, accountable risk ownership, explicit provider
behavior drift, approval expiry reasons, reviewer-quality monitoring, and rollback
coordination. It integrates with
ADR-019 orchestration, ADR-027 providers, ADR-030 indexes, ADR-031 telemetry, ADR-032 memory,
ADR-033 cost, and future ADR-035 cache.

## Database

Requires tenant-scoped risk profiles with accountable owners, candidates, suites, dataset
versions/cases with review/expiry dates, metric and gate policies, runs/results, human
reviews, reviewer-quality snapshots, approvals with expiry reasons, drift signals, and incidents plus a
synthetic-only control-plane template. Detailed DB design must define RLS, indexes,
partitioning, artifact hashes, immutable/superseding evidence, encryption, retention,
effective dates, optimistic concurrency, and large-artifact references.

## Security and Privacy

Adds protected benchmark/holdout storage, evaluation RBAC/ABAC, segregation of duties,
artifact integrity, model-judge/provider processing controls, red-team suites, protected-group
data restrictions, and fail-closed promotion. Evaluation data cannot become a new source of
tenant, employee, prompt, or benchmark-answer leakage.

## Legal, HR, and Compliance

High-impact employment use cases require documented jurisdictional classification,
fairness/accessibility plan, qualified domain/legal review, meaningful human oversight,
contest/appeal path, known limitations, and post-deployment monitoring. This ADR does not
replace jurisdiction-specific legal advice or assessment.

## Performance and Cost

Formal suites consume model, vector, evaluator, storage, and human-review capacity.
Deterministic-first execution, risk-based scheduling, immutable result reuse, and ADR-033
budgets control cost without removing mandatory evidence. Promotion reports include latency
tails and capacity/fallback behavior.

## Development and Delivery

Requires Business, Technical, Database, UI, Test, Security, Privacy/Legal where applicable,
and OpenAPI documentation before code. CI/CD must block promotion based on signed/immutable
gate output, and deployment automation must bind the evaluated bundle hash exactly.

## Operations

Operations owns evaluation capacity, queue health, evaluator availability, canary controls,
dataset-review/expiry, provider-behavior-drift, reviewer-quality, approval-expiry alerts,
rollback rehearsal, and runbooks. Product/AI and domain owners
own quality/risk thresholds; Security/Privacy own adversarial/data controls; Legal/HR own
high-impact employment review; accountable approvers own residual-risk acceptance.

---

# Official and Primary References

- NIST AI Risk Management Framework:
  `https://www.nist.gov/itl/ai-risk-management-framework`
- NIST AI RMF Playbook:
  `https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook`
- NIST AI 600-1, Generative AI Profile:
  `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`
- ISO/IEC 42001:2023 AI management systems overview:
  `https://www.iso.org/standard/81230.html`
- OWASP Top 10 for LLM/GenAI Applications:
  `https://genai.owasp.org/llm-top-10/`
- OWASP prompt injection risk:
  `https://genai.owasp.org/llmrisk/llm01-prompt-injection/`
- Regulation (EU) 2024/1689 (EU AI Act), official text:
  `https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng`
- RAGAS paper, automated evaluation of retrieval-augmented generation:
  `https://arxiv.org/abs/2309.15217`
- Anthropic guidance on success criteria and evaluations:
  `https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests`
- OpenAI evaluation guide:
  `https://platform.openai.com/docs/guides/evals`

The provider guidance illustrates evaluation mechanics only and does not create a provider
dependency. Legal/regulatory applicability must be revalidated for each jurisdiction and
use case before implementation and production activation.

References last validated: 2026-06-25.

---

# Approval

Solution Architect: Approved (Codex)  
Prompt/Context Architect: Architecture controls incorporated  
Security Architect: Security controls incorporated  
Privacy/Legal Reviewer: Privacy/legal controls incorporated  
HR/Payroll Domain Owner: Domain controls incorporated  
Operations Architect: Operational controls incorporated  
Product Owner: Bhajan Lal - Approved 2026-06-25

(Status: Approved)
