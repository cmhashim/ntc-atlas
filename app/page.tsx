import Atlas from '@/components/explorer/atlas';

// The whole atlas is prerendered once and runs client-side over bundled JSON.
export const dynamic = 'force-static';

export default function Home(){return <Atlas/>;}
