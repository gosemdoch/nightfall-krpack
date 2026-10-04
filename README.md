# NightfallCraft 한국어 패치 플러스 (KRtrans-plus)

NightfallCraft - The Casket of Reveries (1.20.1 Forge) 용 한국어 리소스팩입니다.

- **원본**: 디시인사이드 마인크래프트 갤러리 [steve/372364](https://gall.dcinside.com/mgallery/board/view/?id=steve&no=372364) 의 `NightfallCraft 2.0.11 KRtrans.zip` (AI 번역 + 퀘스트·상호작용 수동 보정, 원작자 게시물 참고). 이 저장소는 그 패치를 그대로 포함하고 그 위에 누락분을 보강한 것입니다.
- **보강분** (2.2.9.7 서버 기준 스캔, 2,557개 문구): 퀘스트 텍스트 72개 · FTB Quests UI 583 · Find me 478 · Battle Towers 213 · Aether 1,127 · AzureLib 52 · 그 외 소량 모드 7개
- 퀘스트 키의 영어 원문은 모드팩 전용 모드 `tcrcore` 의 `ftb_translations` 에서 가져왔습니다

## 사용

`NightfallCraft-KRtrans-plus.zip` 을 `.minecraft/resourcepacks/` 에 넣고 리소스팩에서 켭니다. 서버에 접속하면 서버 리소스팩으로도 자동 제안됩니다.

## 구조

- `maps/kr-map-*.json` — 영어 문장 → 한국어 대응표 (수정은 여기서)
- `maps/kr-missing-*.json` — 스캔으로 뽑은 모드별 미번역 원문
- `tools/kr-build.py` — `fill` (대응표로 채우기) · `pending <mod>` (남은 문장) · `pack` (zip 생성)

오역 제보·수정 환영합니다.
