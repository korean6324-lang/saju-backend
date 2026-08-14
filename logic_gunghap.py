'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import BaziChart from '@/components/result/BaziChart';

export default function ResultPage() {
    const router = useRouter();
    const [resData, setResData] = useState<any>(null);

    useEffect(() => {
        const storedData = sessionStorage.getItem('baziResult');
        if (storedData) {
            try {
                setResData(JSON.parse(storedData));
            } catch (e) {
                router.push('/');
            }
        } else {
            router.push('/');
        }
    }, [router]);

    if (!resData) return <div className="min-h-screen bg-[#0a0a0c] flex items-center justify-center text-[#d4af37]">데이터 로딩중...</div>;

    const safeString = (val: any) => {
        if (val === null || val === undefined) return "-";
        if (typeof val === 'string' || typeof val === 'number') return val;
        return JSON.stringify(val); 
    };

    const extractScore = (obj: any) => {
        if (typeof obj === 'number') return obj;
        if (typeof obj === 'object' && obj !== null) {
            if ('score' in obj) return obj.score;
            if ('total_score' in obj) return obj.total_score;
            if ('power' in obj) return obj.power;
            if ('point' in obj) return obj.point;
            if ('value' in obj) return obj.value;
            const numericVal = Object.values(obj).find(v => typeof v === 'number');
            if (numericVal !== undefined) return numericVal;
        }
        return null;
    };

    // 🚨 [핵심 유지] 브라우저 멈춤(Freeze) 현상 원천 차단
    const findDeepData = (obj: any, keywords: string[], depth = 0): any => {
        if (depth > 5) return null; 
        if (!obj || typeof obj !== 'object' || Array.isArray(obj)) return null; 
        
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                if (keywords.some(k => key.toLowerCase().includes(k))) {
                    if (obj[key] !== null && typeof obj[key] === 'object' && Object.keys(obj[key]).length > 0) return obj[key];
                    if (typeof obj[key] === 'string' && obj[key].length > 5) return obj[key];
                }
                if (obj[key] !== null && typeof obj[key] === 'object') {
                    const found = findDeepData(obj[key], keywords, depth + 1);
                    if (found) return found;
                }
            }
        }
        return null;
    };

    const baziData = resData.bazi_data || resData.m_bazi || resData;
    const hiddenStems = resData.hidden_stems;
    const analysis = resData.analysis_result || {};
    
    // 🚨 비전 명리 및 풍수지리(fengshui) 데이터 추출 추가
    const { 
        strength, geokguk, yongshin, practical, mechanics, 
        elements_imbalance, dynamics, unse, timeline, classical, 
        napeum_reading, ideal_partner, secret_readings, fengshui
    } = analysis;

    const yongshinDesc = yongshin?.reason || yongshin?.desc || yongshin?.description || yongshin?.advice || yongshin?.solution || "처방 데이터가 없습니다.";
    
    const gunghap = resData.gunghap || analysis.gunghap;
    const isPartnerMatched = !!gunghap && typeof gunghap === 'object' && Object.keys(gunghap).length > 0;

    const idealMatchData = findDeepData(analysis, ['romance', 'partner', 'ideal', 'love', 'spouse', 'marriage']) || 
                           "나만의 고유한 기운을 보완해 줄 수 있는 오행을 가진 사람을 만나는 것이 좋습니다.";
    
    const wealthData = findDeepData(analysis, ['wealth', 'money', 'finance', 'asset', 'rich']) || 
                       "성실함과 꾸준함으로 자산을 축적하는 흐름입니다.";

    const renderObjectData = (data: any) => {
        if (!data) return null;
        if (typeof data === 'string') return <p>{data}</p>;
        return Object.entries(data).map(([k, v]: [string, any], i) => {
            if (k === 'score' || k === 'value' || typeof v === 'object') return null;
            return <p key={i} className="mb-1"><strong className="text-white capitalize">{k.replace('_', ' ')}:</strong> {safeString(v)}</p>;
        });
    };

    let parsedClassical: any[] = [];
    if (classical?.reading) {
        if (typeof classical.reading === 'string') {
            try { parsedClassical = JSON.parse(classical.reading); } 
            catch (e) { parsedClassical = [{ section: "종합 해석", items: [{ text: classical.reading }] }]; }
        } else if (Array.isArray(classical.reading)) {
            parsedClassical = classical.reading;
        }
    }

    return (
        <div className="bg-[#0a0a0c] min-h-screen text-gray-300 font-sans pb-20">
            <header className="bg-[#111318] border-b border-gray-800 p-6 flex justify-between items-center shadow-xl">
                <div>
                    <h1 className="text-2xl font-black text-[#d4af37]">MYEONGRI MASTER</h1>
                    <div className="text-xs text-gray-500 mt-1 uppercase">Engine V4.0 | TS: {safeString(resData.metadata?.true_solar_time)}</div>
                </div>
                <button onClick={() => router.push('/')} className="px-5 py-2 bg-linear-to-r from-[#b5952f] to-[#d4af37] text-black font-black text-xs uppercase rounded transition-colors shadow-lg hover:scale-105">
                    New Scan
                </button>
            </header>

            <div className="max-w-6xl mx-auto p-4 md:p-6 mt-4 flex flex-col gap-6">
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2 bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden">
                        <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800">
                            <h2 className="text-sm font-bold text-[#d4af37]">1. Core Bazi Matrix (명식 엔진)</h2>
                        </div>
                        <div className="p-4">
                            {baziData && <BaziChart baziData={baziData} />}
                            <div className="mt-6 pt-4 border-t border-gray-800">
                                <h3 className="text-xs text-gray-500 font-bold mb-3 uppercase">Hidden Stems (지장간)</h3>
                                <div className="grid grid-cols-4 gap-2 text-center text-sm font-mono">
                                    {['year', 'month', 'day', 'hour'].map(pillar => (
                                        <div key={pillar} className="bg-[#0a0a0c] p-3 rounded border border-gray-800">
                                            <div className="text-gray-600 text-[10px] mb-1 uppercase font-bold">{pillar}</div>
                                            <div className="text-[#3498db] text-xs">{hiddenStems?.[pillar]?.initial?.join(', ') || '-'}</div>
                                            <div className="text-[#2ecc71] text-xs">{hiddenStems?.[pillar]?.middle?.join(', ') || '-'}</div>
                                            <div className="text-[#e74c3c] font-bold text-sm mt-1">{hiddenStems?.[pillar]?.main?.join(', ') || '-'}</div>
                                        </div>
                                    ))}
                                </div>
                                
                                {mechanics?.tonggeun && (
                                    <div className="mt-4 bg-[#0a0a0c] p-4 rounded-lg border border-gray-800 shadow-inner">
                                        <div className="flex justify-between items-center mb-2">
                                            <strong className="text-[#d4af37] text-xs uppercase">일간 통근 (나의 에너지 뿌리)</strong>
                                            <span className="bg-blue-900/30 text-blue-400 text-[11px] px-2.5 py-1 rounded-full border border-blue-900/50 font-bold font-mono">
                                                TOTAL POWER: {mechanics.tonggeun.total_power || 0}
                                            </span>
                                        </div>
                                        {mechanics.tonggeun.is_rooted && Array.isArray(mechanics.tonggeun.roots) && mechanics.tonggeun.roots.length > 0 ? (
                                            <div className="flex flex-wrap gap-2 mt-2">
                                                {mechanics.tonggeun.roots.map((r: any, idx: number) => (
                                                    <span key={idx} className="text-[10px] text-gray-300 bg-[#111318] px-2.5 py-1.5 rounded border border-gray-700 shadow-sm flex items-center gap-1">
                                                        <span className="text-gray-500">{r.pillar}</span>
                                                        <span className="font-bold text-white">{r.branch}</span>
                                                        <span className="text-[#2ecc71] ml-1">{r.type}</span>
                                                        <span className="font-bold text-[#e74c3c]">{r.hidden_stem}</span>
                                                        <span className="text-blue-400 font-mono ml-1">(+{r.power})</span>
                                                    </span>
                                                ))}
                                            </div>
                                        ) : (
                                            <div className="text-[11px] text-red-400 mt-2 bg-red-950/20 p-2 rounded border border-red-900/30">
                                                뿌리가 튼튼하게 내리지 못했습니다 (無根). 주변 환경 변화에 휩쓸리지 않는 강인한 주관 확립이 필요합니다.
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden flex flex-col">
                        <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800">
                            <h2 className="text-sm font-bold text-[#d4af37]">2. Energy & Balance (에너지/그릇)</h2>
                        </div>
                        <div className="p-4 flex-1 flex flex-col gap-4">
                            
                            <div className="bg-[#0a0a0c] p-4 rounded border border-gray-800">
                                <div className="flex justify-between items-center mb-2 border-b border-gray-800/50 pb-2">
                                    <span className="text-xs text-gray-500 font-bold uppercase tracking-widest">에너지 (신강/신약)</span>
                                    <div className="text-right">
                                        <span className="font-bold text-white text-sm">{safeString(strength?.status || strength?.name || strength)}</span>
                                        {extractScore(strength) !== null && <span className="ml-2 inline-block bg-red-900/20 text-[#e74c3c] px-2 py-0.5 rounded text-[11px] font-mono border border-red-900/50">POWER: {extractScore(strength)}</span>}
                                    </div>
                                </div>
                                <div className="text-gray-400 text-xs leading-relaxed font-light">
                                    {safeString(strength?.desc || strength?.description || "사주의 전체적인 기운과 체급을 나타냅니다.")}
                                </div>
                            </div>

                            <div className="bg-[#0a0a0c] p-4 rounded border border-gray-800">
                                <div className="flex justify-between items-center mb-2 border-b border-gray-800/50 pb-2">
                                    <span className="text-xs text-gray-500 font-bold uppercase tracking-widest">격국 (사회적 그릇)</span>
                                    <div className="text-right">
                                        <span className="font-bold text-[#3498db] text-sm">{safeString(geokguk?.name_clean || geokguk?.name)}</span>
                                        {extractScore(geokguk) !== null && <span className="ml-2 inline-block bg-blue-900/20 text-[#3498db] px-2 py-0.5 rounded text-[11px] font-mono border border-blue-900/50">SCORE: {extractScore(geokguk)}</span>}
                                    </div>
                                </div>
                                <div className="text-gray-400 text-xs leading-relaxed font-light">
                                    {safeString(geokguk?.desc || geokguk?.description || geokguk?.characteristics || "당신의 사회적 역할과 타고난 무기를 의미합니다.")}
                                </div>
                            </div>

                            <div className="bg-[#0a0a0c] p-4 rounded border border-gray-800">
                                <div className="flex justify-between items-center mb-2 border-b border-gray-800/50 pb-2">
                                    <span className="text-xs text-gray-500 font-bold uppercase tracking-widest">수호신 (용신)</span>
                                    <div className="text-right">
                                        <span className="font-bold text-[#2ecc71] text-sm">{safeString(yongshin?.yongshin || yongshin?.name)}</span>
                                        {extractScore(yongshin) !== null && <span className="ml-2 inline-block bg-green-900/20 text-[#2ecc71] px-2 py-0.5 rounded text-[11px] font-mono border border-green-900/50">POWER: {extractScore(yongshin)}</span>}
                                    </div>
                                </div>
                                <div className="text-gray-400 text-xs leading-relaxed font-light mb-2">
                                    {safeString(yongshin?.desc || yongshin?.description || "사주의 불균형을 해결해 주는 가장 핵심적인 기운입니다.")}
                                </div>
                                <div className="text-[11px] text-[#d4af37] bg-yellow-900/10 p-2 rounded border border-yellow-900/30 leading-relaxed">
                                    <strong>💡 처방/솔루션:</strong> {safeString(yongshinDesc)}
                                </div>
                            </div>
                            
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden">
                        <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800 flex justify-between">
                            <h2 className="text-sm font-bold text-[#d4af37]">3. Elements & Health (오행/건강)</h2>
                            {mechanics?.gongmang && mechanics.gongmang !== "-" && (
                                <span className="text-[10px] bg-red-900/30 text-red-400 px-2 py-0.5 rounded border border-red-900/50 font-bold">
                                    공망: {Array.isArray(mechanics.gongmang) ? mechanics.gongmang.join(', ') : mechanics.gongmang}
                                </span>
                            )}
                        </div>
                        <div className="p-4">
                            {mechanics?.elements_dist && (
                                <div className="flex gap-1 mb-5">
                                    {['목', '화', '토', '금', '수'].map(el => (
                                        <div key={el} className="flex-1 bg-[#0a0a0c] p-2 rounded border border-gray-800 text-center relative overflow-hidden">
                                            <div className="text-[10px] text-gray-500 mb-1">{el}</div>
                                            <div className={`font-mono text-lg font-bold ${mechanics.elements_dist[el] === 0 ? 'text-red-500' : 'text-white'}`}>
                                                {safeString(mechanics.elements_dist[el])}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                            <div className="space-y-3">
                                {Array.isArray(practical?.health) && practical.health.find((h:any) => h.element === '종합') && (
                                    <div className="bg-blue-900/10 p-4 rounded-lg border-l-4 border-[#3498db] mb-2">
                                        <div className="text-[#3498db] font-bold text-[12px] mb-1">✨ [종합 건강 리포트]</div>
                                        <div className="text-gray-300 text-[12px] leading-relaxed">
                                            {practical.health.find((h:any) => h.element === '종합').advice}
                                        </div>
                                    </div>
                                )}
                                
                                {Array.isArray(elements_imbalance) && elements_imbalance.length > 0 ? elements_imbalance.map((warn: any, idx: number) => (
                                    <div key={idx} className="bg-red-950/20 p-4 rounded-lg border border-red-900/30">
                                        <div className="flex items-center gap-2 mb-2">
                                            <span className="text-red-400 font-bold text-sm">[{warn.element} 기운 {warn.type}]</span>
                                            {warn.organ && (
                                                <span className="text-gray-400 text-[10px] bg-[#0a0a0c] px-2 py-0.5 rounded border border-gray-800 shadow-sm">
                                                    주의 장기: {warn.organ}
                                                </span>
                                            )}
                                        </div>
                                        {warn.symptom && <div className="text-red-300 text-[11px] mb-2 font-bold tracking-wide">⚠️ 예상 증상: {warn.symptom}</div>}
                                        <div className="text-gray-400 text-[12px] leading-relaxed">{warn.desc || warn.advice}</div>
                                    </div>
                                )) : <div className="text-xs text-gray-500 p-3 bg-[#0a0a0c] rounded border border-gray-800">심각한 오행 불균형이 없습니다.</div>}
                            </div>
                        </div>
                    </div>

                    <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden flex flex-col">
                        <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800">
                            <h2 className="text-sm font-bold text-[#d4af37]">4. Career & Active Disasters (직업/흉살)</h2>
                        </div>
                        <div className="p-4 flex-1 flex flex-col gap-4">
                            
                            <div className="bg-[#0a0a0c] p-5 rounded-lg border border-gray-800 shadow-inner">
                                <div className="text-[13px] font-bold text-[#9b59b6] mb-3 uppercase border-b border-gray-800 pb-2">
                                    💼 핵심 직무 스타일: {safeString(practical?.career?.core_trait)}
                                </div>
                                <div className="mb-4">
                                    <span className="text-[10px] text-gray-500 font-bold block mb-1">추천 직업 및 직군</span>
                                    <div className="text-gray-300 text-[12px] leading-relaxed bg-[#111318] p-3 rounded border border-gray-800">
                                        {safeString(practical?.career?.recommended_jobs)}
                                    </div>
                                </div>
                                {practical?.career?.work_environment && (
                                    <div>
                                        <span className="text-[10px] text-gray-500 font-bold block mb-1">최적의 근무 환경 (용신 기반 처방)</span>
                                        <div className="text-[#2ecc71] text-[12px] leading-relaxed bg-green-950/10 p-3 rounded border border-green-900/20">
                                            {safeString(practical?.career?.work_environment)}
                                        </div>
                                    </div>
                                )}
                            </div>
                            
                            <div className="flex-1 border-t border-gray-800 pt-4 mt-2">
                                <h3 className="text-[11px] text-gray-500 mb-3 uppercase font-bold">발현된 흉살 및 상호작용</h3>
                                <div className="flex flex-col gap-3">
                                    {Array.isArray(dynamics?.disasters) && dynamics.disasters.length > 0 ? dynamics.disasters.map((d: any, i: number) => (
                                        <div key={`d-${i}`} className="bg-purple-900/10 p-3 rounded border border-purple-900/30">
                                            <div className="flex items-center gap-2 mb-1">
                                                <span className="text-[#9b59b6] font-bold text-sm">{typeof d === 'string' ? d : d.name}</span>
                                                {d.hanja_clean && <span className="text-gray-500 text-[10px] font-serif">{d.hanja_clean}</span>}
                                                {d.position && <span className="text-gray-400 text-[10px] bg-[#0a0a0c] px-1.5 py-0.5 rounded border border-gray-800 ml-auto">{d.position}</span>}
                                            </div>
                                            {d.desc && <div className="text-gray-400 text-[11px] leading-relaxed whitespace-pre-wrap">{d.desc}</div>}
                                        </div>
                                    )) : <span className="text-xs text-gray-500">발견된 주요 흉살이 없습니다.</span>}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden">
                    <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800 flex justify-between items-center">
                        <h2 className="text-sm font-bold text-[#e74c3c]">5. Romance & Wealth (최고의 궁합 & 재물운)</h2>
                        {isPartnerMatched ? (
                            <span className="text-[10px] bg-red-900/30 text-red-400 px-2 py-0.5 rounded border border-red-900/50">V4 MATCH ENGINE</span>
                        ) : (
                            <span className="text-[10px] bg-pink-900/30 text-pink-400 px-2 py-0.5 rounded border border-pink-900/50">IDEAL MATCH</span>
                        )}
                    </div>
                    <div className="p-4 md:p-6">
                        {isPartnerMatched ? (
                            <div className="flex flex-col gap-6">
                                {gunghap.my_star && gunghap.partner_star && (
                                    <div className="bg-[#0a0a0c] p-4 rounded border border-gray-800 flex justify-between items-center shadow-inner">
                                        <div className="text-center flex-1">
                                            <div className="text-[10px] text-gray-500 mb-1 font-bold uppercase">나의 본명성</div>
                                            <div className="text-[#3498db] font-bold text-sm">{gunghap.my_star.name}</div>
                                            <div className="text-xs text-gray-500 font-serif">{gunghap.my_star.hanja}</div>
                                        </div>
                                        <div className="text-gray-600 text-[10px] font-black px-4 italic">VS</div>
                                        <div className="text-center flex-1">
                                            <div className="text-[10px] text-gray-500 mb-1 font-bold uppercase">상대의 본명성</div>
                                            <div className="text-[#e84393] font-bold text-sm">{gunghap.partner_star.name}</div>
                                            <div className="text-xs text-gray-500 font-serif">{gunghap.partner_star.hanja}</div>
                                        </div>
                                    </div>
                                )}

                                {Array.isArray(gunghap.fatal_warnings) && gunghap.fatal_warnings.length > 0 && (
                                    <div className="bg-red-950/30 border border-red-900/50 p-4 rounded-lg">
                                        <h3 className="text-red-500 font-bold text-[11px] mb-2 flex items-center gap-2">⚠️ FATAL WARNING (치명적 흉살 경고)</h3>
                                        <ul className="list-disc pl-5 space-y-2">
                                            {gunghap.fatal_warnings.map((warn: string, i: number) => (
                                                <li key={i} className="text-red-300 text-xs leading-relaxed">{warn}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    {gunghap.gugung_matrix && typeof gunghap.gugung_matrix === 'object' && (
                                        <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800 border-t-2 border-t-[#e84393]">
                                            <div className="text-[10px] text-gray-500 mb-2 font-bold uppercase">64구궁팔괘 매트릭스</div>
                                            <div className="text-[#e84393] font-bold text-lg mb-2">{safeString(gunghap.gugung_matrix.status)}</div>
                                            <div className="text-gray-300 text-xs leading-relaxed mb-3">{safeString(gunghap.gugung_matrix.desc)}</div>
                                            <div className="text-gray-500 text-[10px] font-serif border-t border-gray-800 pt-2">"{safeString(gunghap.gugung_matrix.classical)}"</div>
                                        </div>
                                    )}

                                    {gunghap.elemental_salvation && typeof gunghap.elemental_salvation === 'object' && (
                                        <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800 border-t-2 border-t-[#2ecc71]">
                                            <div className="text-[10px] text-gray-500 mb-2 font-bold uppercase">오행 구원 및 조후 보완</div>
                                            <div className="flex items-center gap-2 mb-2">
                                                <div className="text-[#2ecc71] font-bold text-lg">상생 조화력</div>
                                                <span className="bg-green-900/30 text-green-400 text-[10px] px-2 py-0.5 rounded border border-green-900/50">SCORE: {safeString(gunghap.elemental_salvation.score)}</span>
                                            </div>
                                            <div className="text-gray-300 text-xs leading-relaxed">{safeString(gunghap.elemental_salvation.desc)}</div>
                                        </div>
                                    )}
                                </div>

                                {gunghap.match_3d && typeof gunghap.match_3d === 'object' && (
                                    <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800">
                                        <h3 className="text-xs text-[#d4af37] font-bold mb-4 uppercase">입체적(3D) 속궁합 분석</h3>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div className="bg-[#111318] p-4 rounded border border-gray-800">
                                                <div className="text-[10px] text-gray-500 mb-1 font-bold">정신적 교감 (천간)</div>
                                                <div className="text-blue-400 font-bold text-sm mb-2">{safeString(gunghap.match_3d.mental?.status)}</div>
                                                <div className="text-gray-400 text-xs leading-relaxed">{safeString(gunghap.match_3d.mental?.desc)}</div>
                                            </div>
                                            <div className="bg-[#111318] p-4 rounded border border-gray-800">
                                                <div className="text-[10px] text-gray-500 mb-1 font-bold">육체적 결합 (지지)</div>
                                                <div className="text-pink-400 font-bold text-sm mb-2">{safeString(gunghap.match_3d.physical?.status)}</div>
                                                <div className="text-green-400 text-xs mb-1">장점: {safeString(gunghap.match_3d.physical?.pros)}</div>
                                                <div className="text-red-400 text-xs">단점: {safeString(gunghap.match_3d.physical?.cons)}</div>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 gap-6">
                                {analysis.my_star && (
                                    <div className="bg-[#0a0a0c] p-4 rounded border border-gray-800 flex justify-between items-center shadow-sm">
                                        <span className="text-[10px] text-gray-500 font-bold uppercase">나의 타고난 본명성(별자리)</span>
                                        <div className="text-right">
                                            <span className="text-[#3498db] font-bold text-sm">{analysis.my_star.name}</span>
                                            <span className="text-gray-500 text-xs ml-2 font-serif">{analysis.my_star.hanja}</span>
                                        </div>
                                    </div>
                                )}

                                <div className="bg-[#0a0a0c] p-5 md:p-6 rounded border border-gray-800 border-t-2 border-t-[#e84393] shadow-lg">
                                    <h3 className="text-[12px] text-[#e84393] mb-4 font-bold uppercase flex items-center gap-2 border-b border-gray-800 pb-3">
                                        <span>💘 나만의 최고 궁합 (역산형 이상형 처방전)</span>
                                    </h3>
                                    
                                    {ideal_partner && typeof ideal_partner === 'object' ? (
                                        <div className="flex flex-col gap-4">
                                            {Object.entries(ideal_partner).map(([key, val]: [string, any], idx: number) => {
                                                if (key === 'score' || key === 'value') return null;
                                                return (
                                                    <div key={idx} className="bg-[#111318] p-4 rounded border border-gray-800 relative overflow-hidden">
                                                        <div className="text-[11px] text-[#f1c40f] font-bold mb-2 tracking-wide uppercase">
                                                            ■ {key.replace(/_/g, ' ')}
                                                        </div>
                                                        <div className="text-gray-300 text-[12px] leading-loose break-keep">
                                                            {safeString(val)}
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    ) : (
                                        <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                                            {renderObjectData(idealMatchData)}
                                        </div>
                                    )}
                                </div>
                                
                                <div className="bg-[#0a0a0c] p-5 md:p-6 rounded border border-gray-800 border-t-2 border-t-[#f1c40f] shadow-lg">
                                    <h3 className="text-[11px] text-[#f1c40f] mb-3 font-bold uppercase flex items-center gap-2">
                                        <span>💰 재물운 (자산 증식 가이드)</span>
                                    </h3>
                                    <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                                        {renderObjectData(wealthData)}
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {Array.isArray(dynamics?.special_stars) && dynamics.special_stars.length > 0 && (
                    <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden">
                        <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800">
                            <h2 className="text-sm font-bold text-[#d4af37]">6. Special Stars (부위별 귀인 및 길성)</h2>
                        </div>
                        <div className="p-4 md:p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                            {dynamics.special_stars.map((star: any, idx: number) => (
                                <div key={idx} className="bg-[#0a0a0c] p-4 rounded border border-gray-800 border-l-2 border-l-[#f1c40f]">
                                    <div className="flex justify-between items-start mb-2">
                                        <div>
                                            <span className="text-[#f1c40f] font-bold text-sm">{star.name}</span>
                                            {star.hanja_clean && <span className="text-gray-500 text-xs ml-2 font-serif">{star.hanja_clean}</span>}
                                        </div>
                                        {star.position && (
                                            <span className="bg-yellow-900/20 text-[#f1c40f] text-[10px] px-2 py-0.5 rounded border border-yellow-900/30 text-right">
                                                {star.position}
                                            </span>
                                        )}
                                    </div>
                                    {star.desc && <div className="text-gray-400 text-xs leading-relaxed whitespace-pre-wrap">{star.desc}</div>}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden">
                    <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800">
                        <h2 className="text-sm font-bold text-[#d4af37]">7. Timeline & Realtime Unse (실시간 운세 흐름)</h2>
                    </div>
                    <div className="p-4 md:p-6">
                        {unse && typeof unse === 'object' && (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 items-stretch">
                                
                                <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800 border-t-4 border-t-[#f1c40f] flex flex-col h-full shadow-lg">
                                    <div className="flex justify-between items-center mb-4 pb-3 border-b border-gray-800">
                                        <div className="text-[11px] text-gray-500 uppercase font-black tracking-wider">세운 (올해)</div>
                                        <div className="font-mono text-[#f1c40f] font-bold text-lg">{safeString(unse.year?.stem)}{safeString(unse.year?.branch)}년</div>
                                    </div>
                                    <div className="mb-4">
                                        <div className="text-[#f1c40f] font-bold text-[13px] mb-2">{safeString(unse.year?.overall_status)}</div>
                                        <div className="text-[12px] text-gray-400 leading-relaxed">{safeString(unse.year?.overall_desc)}</div>
                                    </div>
                                    {Array.isArray(unse.year?.events) && unse.year.events.length > 0 && (
                                        <div className="mt-auto pt-3 flex flex-col gap-2">
                                            {unse.year.events.map((ev: any, i: number) => (
                                                <div key={i} className={`p-3 rounded border ${ev.type === 'bad' ? 'bg-red-950/30 border-red-900/50' : 'bg-green-950/30 border-green-900/50'}`}>
                                                    <div className={`font-bold text-[11px] mb-1 ${ev.type === 'bad' ? 'text-red-400' : 'text-green-400'}`}>{ev.title}</div>
                                                    <div className="text-[10px] text-gray-500 leading-snug">{ev.desc}</div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>

                                <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800 border-t-4 border-t-[#e74c3c] flex flex-col h-full shadow-lg">
                                    <div className="flex justify-between items-center mb-4 pb-3 border-b border-gray-800">
                                        <div className="text-[11px] text-gray-500 uppercase font-black tracking-wider">월건 (이달)</div>
                                        <div className="font-mono text-white font-bold text-lg">
                                            <span className="text-[#e74c3c] mr-1 text-sm">{unse.month?.month_num}월</span> 
                                            {safeString(unse.month?.stem)}{safeString(unse.month?.branch)}
                                        </div>
                                    </div>
                                    <div className="mb-4">
                                        <div className="text-[#e74c3c] font-bold text-[13px] mb-2">{safeString(unse.month?.data?.overall_status)}</div>
                                        <div className="text-[12px] text-gray-400 leading-relaxed">{safeString(unse.month?.data?.overall_desc)}</div>
                                    </div>
                                    {Array.isArray(unse.month?.data?.events) && unse.month.data.events.length > 0 && (
                                        <div className="mt-auto pt-3 flex flex-col gap-2">
                                            {unse.month.data.events.map((ev: any, i: number) => (
                                                <div key={i} className={`p-3 rounded border ${ev.type === 'bad' ? 'bg-red-950/30 border-red-900/50' : 'bg-green-950/30 border-green-900/50'}`}>
                                                    <div className={`font-bold text-[11px] mb-1 ${ev.type === 'bad' ? 'text-red-400' : 'text-green-400'}`}>{ev.title}</div>
                                                    <div className="text-[10px] text-gray-500 leading-snug">{ev.desc}</div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>

                                <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800 border-t-4 border-t-[#3498db] flex flex-col h-full shadow-lg">
                                    <div className="flex justify-between items-center mb-4 pb-3 border-b border-gray-800">
                                        <div className="text-[11px] text-gray-500 uppercase font-black tracking-wider">일진 (오늘)</div>
                                        <div className="font-mono text-white font-bold text-lg">
                                            <span className="text-[#3498db] mr-1 text-sm">{unse.day?.day_num}일</span> 
                                            {safeString(unse.day?.stem)}{safeString(unse.day?.branch)}
                                        </div>
                                    </div>
                                    <div className="mb-4">
                                        <div className="text-[#3498db] font-bold text-[13px] mb-2">{safeString(unse.day?.data?.overall_status)}</div>
                                        <div className="text-[12px] text-gray-400 leading-relaxed">{safeString(unse.day?.data?.overall_desc)}</div>
                                    </div>
                                    {Array.isArray(unse.day?.data?.events) && unse.day.data.events.length > 0 && (
                                        <div className="mt-auto pt-3 flex flex-col gap-2">
                                            {unse.day.data.events.map((ev: any, i: number) => (
                                                <div key={i} className={`p-3 rounded border ${ev.type === 'bad' ? 'bg-red-950/30 border-red-900/50' : 'bg-green-950/30 border-green-900/50'}`}>
                                                    <div className={`font-bold text-[11px] mb-1 ${ev.type === 'bad' ? 'text-red-400' : 'text-green-400'}`}>{ev.title}</div>
                                                    <div className="text-[10px] text-gray-500 leading-snug">{ev.desc}</div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

                        {Array.isArray(timeline?.daewun?.timeline) && (
                            <div>
                                <h3 className="text-[11px] text-gray-500 mb-3 uppercase tracking-widest font-bold">10-Year Cycle (대운표)</h3>
                                <div className="flex overflow-x-auto gap-2 pb-2 scrollbar-thin scrollbar-thumb-gray-700">
                                    {timeline.daewun.timeline.map((dw: any, idx: number) => (
                                        <div key={idx} className="min-w-20 bg-[#0a0a0c] p-3 rounded text-center border border-gray-800 flex flex-col items-center">
                                            <div className="text-[10px] text-gray-500 mb-1 font-bold whitespace-nowrap">
                                                {safeString(dw.stem_tg)} / {safeString(dw.branch_tg)}
                                            </div>
                                            <div className="text-lg font-black text-white">{dw.stem}{dw.branch}</div>
                                            <div className="text-[10px] text-[#e74c3c] font-bold mt-1 font-mono">{dw.age}세</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {secret_readings && (
                    <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden">
                        <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800">
                            <h2 className="text-sm font-bold text-[#d4af37]">8. Secret Destiny (귀곡산명술 & 치명적 위기 스캔)</h2>
                        </div>
                        <div className="p-4 md:p-6 flex flex-col gap-6">
                            
                            {/* 귀곡산명술 */}
                            {secret_readings.guiguzi && (
                                <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800 border-t-2 border-t-[#3498db] shadow-sm">
                                    <h3 className="text-[12px] text-[#3498db] mb-3 font-bold uppercase flex items-center gap-2">
                                        <span>📜 귀곡산명술 (연간-시간 조합 비문)</span>
                                    </h3>
                                    <div className="flex items-center gap-3 mb-2">
                                        <span className="bg-blue-900/20 text-[#3498db] px-2 py-1 rounded border border-blue-900/50 font-bold text-xs font-mono">
                                            조합: {secret_readings.guiguzi.combination}
                                        </span>
                                    </div>
                                    <div className="text-gray-300 text-[12px] leading-relaxed break-keep">
                                        {secret_readings.guiguzi.description}
                                    </div>
                                </div>
                            )}

                            {/* 치명적 위기 나이 (천극지충) */}
                            {secret_readings.critical_ages && (
                                <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800 border-t-2 border-t-[#e74c3c] shadow-sm">
                                    <h3 className="text-[12px] text-[#e74c3c] mb-3 font-bold uppercase flex items-center gap-2">
                                        <span>⏳ 천극지충(天剋地沖) 붕괴 위기 연령</span>
                                    </h3>
                                    {secret_readings.critical_ages.ages && secret_readings.critical_ages.ages.length > 0 ? (
                                        <div className="flex gap-2 mb-3">
                                            {secret_readings.critical_ages.ages.map((age: number, idx: number) => (
                                                <span key={idx} className="bg-red-900/30 text-red-400 font-bold text-xs px-3 py-1 rounded border border-red-900/50">
                                                    {age}세
                                                </span>
                                            ))}
                                        </div>
                                    ) : null}
                                    <div className="text-gray-400 text-[12px] leading-relaxed break-keep">
                                        {secret_readings.critical_ages.message}
                                    </div>
                                </div>
                            )}

                            {/* 잠복된 파멸의 흉살 (Secret Patterns) */}
                            {Array.isArray(secret_readings.secret_patterns) && secret_readings.secret_patterns.length > 0 && (
                                <div className="bg-[#0a0a0c] p-5 rounded border border-gray-800 border-t-2 border-t-[#9b59b6] shadow-sm">
                                    <h3 className="text-[12px] text-[#9b59b6] mb-3 font-bold uppercase flex items-center gap-2">
                                        <span>☠️ 원국 내 잠복된 극흉의 살기</span>
                                    </h3>
                                    <div className="flex flex-col gap-3">
                                        {secret_readings.secret_patterns.map((pat: any, idx: number) => (
                                            <div key={idx} className="bg-purple-950/20 p-3 rounded border border-purple-900/30">
                                                <div className="text-[#9b59b6] font-bold text-[11px] mb-1">[{pat.name}]</div>
                                                <div className="text-gray-400 text-[11px] leading-relaxed">{pat.warning}</div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                        </div>
                    </div>
                )}

                {parsedClassical.length > 0 && (
                    <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden">
                        <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800">
                            <h2 className="text-sm font-bold text-[#d4af37]">9. Classical Readings (고전 엔진)</h2>
                        </div>
                        <div className="p-4 md:p-6 flex flex-col gap-6">
                            {parsedClassical.map((block: any, idx: number) => (
                                <div key={idx} className="bg-[#0a0a0c] p-5 md:p-6 rounded border border-gray-800">
                                    {block.section && <h3 className="text-sm font-bold text-[#f1c40f] mb-4 pb-3 border-b border-gray-800/50 uppercase tracking-wide">{block.section}</h3>}
                                    <div className="flex flex-col gap-5">
                                        {Array.isArray(block.items) && block.items.map((item: any, i: number) => (
                                            <div key={i} className="text-sm text-gray-300 leading-loose">
                                                {item.title && (
                                                    <div className="mb-1.5 flex items-end gap-2">
                                                        <strong className="text-white text-sm">[{item.title}]</strong>
                                                        {item.hanja && <span className="text-[11px] text-gray-500 font-serif">{item.hanja}</span>}
                                                    </div>
                                                )}
                                                <p className="text-[13px] text-gray-400 font-light tracking-wide">{item.text}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {Array.isArray(napeum_reading) && napeum_reading.length > 0 && (
                    <div className="bg-[#111318] rounded-xl border border-gray-800 shadow-xl overflow-hidden">
                        <div className="bg-[#1a1c23] px-4 py-3 border-b border-gray-800">
                            <h2 className="text-sm font-bold text-[#d4af37]">10. Napeum Frequency (납음오행 파동)</h2>
                        </div>
                        <div className="p-4 md:p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                            {napeum_reading.map((n: any, idx: number) => (
                                <div key={idx} className="bg-[#0a0a0c] p-4 rounded border border-gray-800">
                                    <div className="text-[#3498db] font-bold text-[11px] mb-1.5 uppercase">{safeString(n?.pillar)} : {safeString(n?.full)}</div>
                                    <div className="text-gray-400 text-xs leading-relaxed">{safeString(n?.desc)}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}