import { Sparkles, Compass, CalendarDays, Wallet, MapPin } from "lucide-react";
import AgentCard from "./AgentCard";

function Stat({ icon, label, value }) {
if (!value) return null;

return ( <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4"> <div className="flex items-center gap-2 text-sm text-slate-400">
{icon}
{label} </div> <div className="mt-2 text-lg font-semibold text-white">
{value} </div> </div>
);
}

export default function FinalResponseCard({ data }) {
const planner = data?.planner || data?.agent_outputs?.planner || {};

return (
<AgentCard
icon={<Sparkles size={22} />}
title="Your trip is ready"
subtitle="VoyagerAI final recommendation"
status="completed"
>
{/* Hero summary */} <div className="rounded-3xl border border-blue-500/20 bg-gradient-to-r from-blue-950/60 via-slate-900 to-cyan-950/40 p-6"> <div className="flex items-center gap-3 mb-4"> <Compass className="h-6 w-6 text-cyan-300" /> <h2 className="text-2xl font-bold text-white">
{planner.destination || "Your trip"} </h2> </div>

```
    <p className="text-slate-200 leading-relaxed text-lg">
      {data.response ||
        "Your personalized travel plan has been generated successfully. The itinerary balances sightseeing, relaxation, local experiences, and travel efficiency."}
    </p>
  </div>

  {/* Quick trip stats */}
  <div className="mt-6 grid gap-4 md:grid-cols-3">
    <Stat
      icon={<MapPin className="h-5 w-5 text-blue-400" />}
      label="Destination"
      value={planner.destination}
    />

    <Stat
      icon={<CalendarDays className="h-5 w-5 text-cyan-400" />}
      label="Duration"
      value={
        planner.duration_days
          ? `${planner.duration_days} days`
          : null
      }
    />

    <Stat
      icon={<Wallet className="h-5 w-5 text-emerald-400" />}
      label="Estimated budget"
      value={
        planner.total_estimated_cost
          ? `₹${planner.total_estimated_cost.toLocaleString()}`
          : null
      }
    />
  </div>

  {/* Highlights */}
  <div className="mt-8">
    <div className="flex items-center gap-2 mb-4">
      <Sparkles className="h-5 w-5 text-cyan-400" />
      <h3 className="text-lg font-semibold text-white">
        Trip highlights
      </h3>
    </div>

    <div className="grid gap-3 md:grid-cols-2">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 text-slate-200">
        Curated day-by-day itinerary
      </div>
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 text-slate-200">
        Optimized travel pacing
      </div>
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 text-slate-200">
        Local food and cultural experiences
      </div>
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 text-slate-200">
        Balanced sightseeing and relaxation
      </div>
    </div>
  </div>

  {/* Travel tip */}
  <div className="mt-8 rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-5">
    <div className="mb-2 flex items-center gap-2">
      <Sparkles className="h-4 w-4 text-emerald-300" />
      <h4 className="font-semibold text-white">
        VoyagerAI recommendation
      </h4>
    </div>

    <p className="leading-relaxed text-slate-200">
      {planner.notes ||
        "Book flights and hotels 3–6 weeks in advance for the best prices, keep one flexible evening in the itinerary, and reserve major experiences in advance during peak season."}
    </p>
  </div>
</AgentCard>


);
}
