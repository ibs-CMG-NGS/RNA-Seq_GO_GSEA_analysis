# 🎯 구조 변경 완료!

## 📁 새로운 프로젝트 구조

```
RNA-Seq_GO_GSEA_analysis/
│
├── 📄 Snakefile_GO                  # GO enrichment 워크플로우
├── 📄 Snakefile_GSEA                # GSEA 워크플로우
├── 📄 Snakefile_batch_GO            # 배치 GO 분석 워크플로우
├── 📄 Snakefile_batch_GSEA          # 배치 GSEA 워크플로우
│
├── 📂 configs/                      # 설정 파일
│   ├── GO_pipeline_Shank2.yaml     # ✏️ 프로젝트별 설정 (편집)
│   ├── GO_pipeline_H2O2.yaml
│   ├── GO_pipeline_CHD8.yaml
│   ├── deg_comparison_*.yaml
│   ├── gene_filter_*.yaml
│   │
│   └── 📂 templates/                # 📋 템플릿 (복사용)
│       ├── go_config.yaml
│       ├── gsea_config.yaml
│       └── batch_go_config_*.yaml
│
├── 📂 docs/                         # 📚 모든 문서
│   ├── CONFIG_STRUCTURE.md
│   ├── WORKFLOW_README.md
│   ├── QUICK_REFERENCE.md
│   ├── API_REFERENCE.md
│   ├── MIGRATION_GUIDE.md
│   └── WORKFLOW_COMPARISON.md
│
├── 📂 scripts/                      # 🔧 헬퍼 스크립트
│   ├── run_go_pipeline.sh
│   ├── run_gsea_pipeline.sh
│   ├── run_snakemake_go.sh
│   └── run_snakemake_gsea.sh
│
├── 📂 src/                          # 🐍 Python 소스 코드
│   └── analysis/
│       ├── data_loading.py
│       ├── filtering.py
│       ├── go_enrich.py
│       ├── go_barplot.py
│       ├── volcano.py
│       └── ...
│
├── 📂 data/                         # 📊 입력 데이터
├── 📂 ref/                          # 📖 참조 파일 (GO, GAF)
├── 📂 output/                       # 📤 분석 결과
└── 📂 results/                      # 📤 배치 결과
```

---

## ✨ 주요 변경사항

### 1. **Snakefile을 루트로 이동**
   - **변경 전**: `workflow/Snakefile_GO`
   - **변경 후**: `Snakefile_GO`
   - **이유**: 더 간단하고 직관적인 접근

### 2. **설정 파일 구조 개선**
   - **변경 전**: 
     - `workflow/config/` (템플릿)
     - `configs/` (프로젝트별)
   - **변경 후**: 
     - `configs/templates/` (템플릿)
     - `configs/` (프로젝트별)
   - **이유**: 모든 설정 파일이 한 곳에

### 3. **문서 통합**
   - **변경 전**: `workflow/README.md`, `CONFIG_STRUCTURE.md` (루트)
   - **변경 후**: 모든 문서가 `docs/`에
   - **이유**: 문서 찾기 쉬움

### 4. **스크립트 통합**
   - **변경 전**: `scripts/`, `workflow/scripts/`
   - **변경 후**: 모든 스크립트가 `scripts/`에
   - **이유**: 중복 제거

---

## 🚀 새로운 사용법

### 이전 방식
```bash
snakemake --snakefile workflow/Snakefile_GO \
          --configfile configs/GO_pipeline_Shank2.yaml \
          --cores 4
```

### 새로운 방식 (더 간단!)
```bash
snakemake --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_Shank2.yaml \
          --cores 4
```

---

## 📝 템플릿 사용법

### 새 프로젝트 설정 생성

```bash
# 1. 템플릿 복사
cp configs/templates/go_config.yaml configs/GO_pipeline_MyProject.yaml

# 2. 편집
nano configs/GO_pipeline_MyProject.yaml

# 3. 실행
snakemake --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_MyProject.yaml \
          --cores 4
```

---

## 🎯 장점

✅ **간결함**: 불필요한 `workflow/` 계층 제거  
✅ **명확함**: Snakefile이 루트에서 바로 보임  
✅ **통합성**: 설정, 문서, 스크립트 각각 한 곳에  
✅ **직관적**: 프로젝트 구조 이해 쉬움  
✅ **유지보수**: 파일 찾기 쉬움

---

## 📖 자세한 정보

- [CONFIG_STRUCTURE.md](docs/CONFIG_STRUCTURE.md) - 설정 파일 가이드
- [WORKFLOW_README.md](docs/WORKFLOW_README.md) - Snakemake 사용법
- [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) - 빠른 참조

---

## 🔄 마이그레이션

기존 코드나 스크립트에서 경로 업데이트 필요:

| 변경 전 | 변경 후 |
|---------|---------|
| `workflow/Snakefile_GO` | `Snakefile_GO` |
| `workflow/config/go_config.yaml` | `configs/templates/go_config.yaml` |
| `workflow/scripts/run_*.sh` | `scripts/run_*.sh` |
| `CONFIG_STRUCTURE.md` | `docs/CONFIG_STRUCTURE.md` |

