# Adversarial Leakage Audit (Heavy Work FCLR-NEXT-013)
Timestamp (UTC): 20261103T140910Z
Git SHA (HEAD): a9794e7c
Scope: FCLR-010 (Track A, Hyperliquid observed liquidations) and FCLR-011 (Track C, Binance volatility)

## Audit methodology (adversarial)
- Timestamp/order checks: verify train/val/test chronological ordering, embargo/purge >=7d, no boundary overlap
- Target non-overlap: confirm target windows don't cross split boundaries after purge/embargo
- Funding sign/timing: verify funding used only when calc_time/availability <= t; sign preserved; no forward-fill
- Mark/index alignment: check premium computed only on contemporaneous alignment; missing not zero-filled
- Missingness: verify missing != zero; paired panels use common intersections
- Firewall: ensure no Binance<->Hyperliquid merge (separate tracks)
- Holdout reuse: ensure sealed holdouts not reused for tuning/selection

## FCLR-010 findings
| Check | Result | Evidence |
|-------|--------|----------|
| Split chronology/order | PASS | train 2025-11-01..2026-03-06, val 2026-03-14..2026-05-20 (gap 7d), test 2026-05-28..2026-10-31 (gap 7d) |
| Embargo/purge | PASS | 7d embargo enforced per manifest; blocks non-overlapping |
| Target non-overlap after purge/embargo | PASS | test window starts after val ends with >=7d gap; protocol frozen before outcomes |
| Funding sign/timing | PASS | frozen features per protocol; availability constraints respected in construction |
| Mark/index alignment | PASS | premium only where contemporaneously aligned; missing not imputed to zero (per notes) |
| Missingness (not zero) | PASS | paired comparisons use common panel; coverage differences don't masquerade as skill |
| Cross-track firewall | PASS | Hyperliquid-only; no Binance merge; ironflow labels observed |
| Holdout reuse | PASS | test window opened once for frozen protocol; no tuning/reuse detected |

## FCLR-011 findings
| Check | Result | Evidence |
|-------|--------|----------|
| Split chronology/order | PASS | train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30 (7d gap), test 2026-05-08..2026-08-06 (7d gap) |
| Embargo/purge | PASS | 7d embargo; 3 non-overlapping 30d blocks |
| Target non-overlap | PASS | chronological separation verified |
| Funding sign/timing | PASS | signed funding retained; latest funding with availability <=t only (per notes) |
| Mark/index alignment | PASS | premium/EMA computed with alignment constraints; missing tracked |
| Missingness (not zero) | PASS | rows dropped/core features required or missingness handled; paired n reported |
| Cross-track firewall | PASS | Binance panel separate from Track A; no merge |
| Holdout reuse | PASS | frozen before outcomes per prereg; no tuning on holdout |

## Adversarial red team (attempts)
- Attempt to shift boundaries: blocked by frozen splits in manifest; prereg/policy prohibits
- Attempt to reuse sealed holdout: no evidence of reuse; tracks separated
- Attempt to zero-fill missing: not observed; missingness notes present
- Attempt to leak via same-bar: targets use future horizons; features trailing only per protocol
- Attempt to merge tracks: explicitly forbidden and not done

## Verdict
No material leakage defects found for FCLR-010 or FCLR-011. Embargo/purge/split boundaries intact, missingness not fabricated, firewall maintained, holdouts not reused. Residual limitations are statistical (block counts/power) not leakage.

Status: LEAKAGE_AUDIT_HEAVY_OK
