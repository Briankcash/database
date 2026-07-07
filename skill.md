# Skill: PayKool 迎新推廣 Code + Offer Matcher

## Purpose
Read PayKool promotion pages and reply with the correct **迎新推廣** invitation/promo code and discount/reward offer based on T&C.

## Source
- Index: `https://www.paykool.hk/promotions`
- Detail pages: `https://www.paykool.hk/promotions/<slug>`

## Extracted 迎新 Promotion Map (from current website)
Use this as a quick lookup, then verify live page T&C before final answer.

| Slug | Promotion Code | Offer (summary) |
|---|---|---|
| `Starbucks2026` | `PPSB` | up to HK$500 Starbucks e-cash voucher |
| `rebate` | `REBATE` | 10% spending rebate, up to HK$500 |
| `travel360` | `PPAT360` | HK$300 e-discount voucher |
| `akiv` | `PPAKIV` | HK$400 card spending credit |
| `athome` | `PPHOME` | HK$400 electronic discount voucher |
| `friendlyfaretaxi` | `PPFFT` | HK$400 welcome reward |
| `Giormani` | `M2PCCGIORMANI` | HK$500 welcome reward |
| `jumpingym` | `JG` | HK$100 spending credit |
| `mbmakersoul` | `MBMAKERSOUL` | $500 spending credit |
| `mbsim` | `MBSIM` | HK$288 credit + Asia data SIM reward |
| `ppjhc2026` | `PPJHCWEB` | $300 reward |
| `pizzahut202602` | `PPPZH` | $400 welcome reward |
| `ppdeco` | `PPDECO` | up to HK$1,800 reward |
| `pphad` | `PPHAD` | $500 spending credit (under qualifying spend) |
| `pplab` | `PPLAB` | up to HK$400 welcome reward |
| `ppsta` | `PPSTA` | up to HK$300 reward |
| `ppwaf` | `PPWAF` | $388 spending credit |
| `ppwlsf` | `PPWLSF` | up to HK$500 welcome reward |
| `ppyuk` | `PPYUK` | up to $500 discount |
| `cardertoysnplace` | `MBCARDER` | HK$1 designated card-box coupon |

## Input Required
1. Promotion slug/URL or merchant name.
2. User status: new customer or existing customer.
3. Application date and approval date (if available).
4. Spend amount, merchant, and payment channel.

## Decision Rules
1. Open the exact promotion detail page.
2. Confirm all required T&C fields: period, eligibility, spend threshold, cap, and exclusions.
3. Match user case against the promotion map and live T&C.
4. If required data is missing, return `UNCLEAR` and ask for only missing fields.
5. If website text and map conflict, **live page T&C wins**.

## Output Format
- `decision`: ELIGIBLE | NOT_ELIGIBLE | UNCLEAR
- `promotion_url`
- `promotion_code`
- `offer`
- `why` (2-5 bullets, T&C-based)
- `missing_information` (if any)
- `next_action`
- `disclaimer`: Final approval is subject to PayKool official T&C and system records.

## Reply Template
1. **Result:** `<decision>`
2. **Code & Offer:** `<promotion_code>` + `<offer>`
3. **Why:** bullet points mapped to T&C
4. **Next step:** exact action (apply/redeem/provide missing info)
