import NLUCard from "../Cards/NLUCard";
import PlannerCard from "../Cards/PlannerCard";
//import HotelCard from "../Cards/HotelCard";
//import WeatherCard from "../Cards/WeatherCard";
//import FlightCard from "../Cards/FlightCard";
//import GeneralCard from "../Cards/GeneralCard";

export default function Message({ message }) {
  if (message.sender === "user") {
    return (
      <div className="flex justify-end mb-6">
        <div className="bg-blue-600 text-white rounded-2xl px-5 py-4 max-w-xl">
          {message.text}
        </div>
      </div>
    );
  }

  switch (message.node) {
    case "nlu":
      return <NLUCard data={message.output} />;

    case "plan_trip":
    case "planner":
      return <PlannerCard data={message.output} />;

    case "hotel_search":
    case "hotel":
      return <HotelCard data={message.output} />;

    case "weather":
      return <WeatherCard data={message.output} />;

    case "flight_search":
    case "flight":
      return <FlightCard data={message.output} />;

    case "general":
      return <GeneralCard data={message.output} />;

    default:
      return null;
  }
}