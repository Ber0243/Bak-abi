#!/usr/bin/env bash
# Kullanım: bash scripts/ci-build.sh   (ios-kabuk klasöründen ya da herhangi bir yerden)
set -euo pipefail
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
cd "$(dirname "$0")/.."
mkdir -p build
exec > >(tee "build/log.txt") 2>&1
echo "== TÜRKAİ kabuk derlemesi =="

rm -rf ios build/derived build/Payload build/TURKAI-imzasiz.ipa
npm install --no-audit --no-fund
npx cap add ios
python3 scripts/patch_ios.py

cd ios/App
xcodebuild -workspace App.xcworkspace -scheme App -configuration Release \
  -sdk iphoneos -destination 'generic/platform=iOS' \
  -derivedDataPath "$PWD/../../build/derived" \
  CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY="" \
  build
cd ../..

APP="$(find build/derived/Build/Products -maxdepth 2 -type d -name 'App.app' | grep 'Release-iphoneos' | head -1)"
[ -n "$APP" ] || { echo "App.app bulunamadı"; exit 1; }
mkdir -p build/Payload
cp -R "$APP" build/Payload/
( cd build && zip -qry TURKAI-imzasiz.ipa Payload )
unzip -l build/TURKAI-imzasiz.ipa | tail -n 3
echo "IPA hazır"
[ -z "${GITHUB_STEP_SUMMARY:-}" ] || echo "IPA hazır: TURKAI-imzasiz.ipa" >> "$GITHUB_STEP_SUMMARY"
