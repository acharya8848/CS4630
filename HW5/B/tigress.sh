#!/usr/bin/env zsh

tigress --Environment=x86_64:Linux:Gcc \
	--Seed=42 \
	--Transform=Split \
	--SplitKinds=top \
	--Functions=main \
	--Transform=Flatten \
	--FlattenDispatch=switch \
	--FlattenOpaqueStructs=array \
	--FlattenObfuscateNext=false \
	--FlattenSplitBasicBlocks=false \
	--Functions=ackermann \
	--out=ackermann2.c ackermann.c