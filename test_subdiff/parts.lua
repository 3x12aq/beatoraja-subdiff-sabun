local parts = {}

local OP_SUBDIFF_OFF	= get_property_op()
local OP_SUBDIFF_ON	= get_property_op()
local TIMER_SUBDIFF	= get_customTimer_id()

parts.property = {
	{name = "subdiff", item = {
		{name = "OFF",	op = OP_SUBDIFF_OFF},
		{name = "ON",	op = OP_SUBDIFF_ON}
	},def = "ON"}
}

parts.filepath = {}
parts.offset = {}

local function load()

	if skin_config.option["subdiff"] == OP_SUBDIFF_ON then
        if SUBDIFF_TABLE == nil then
          SUBDIFF_TABLE = {}
          local chunk, err = loadfile("customize/subdiff/subdiff.lua")
          if chunk then
            SUBDIFF_TABLE = chunk()
          end
        end
	
		local now_song = {
			md5 = "",
			sha256 = "",
		}
		local display = {
            subdiff = "...",
		}
		
		parts.source = {
			-- {id = "src-analysis", path = "customize/advanced/test_bmsanal/parts.png"}
		}
		parts.font = {}
		parts.image = {
			-- {id = "ui-analysis", src = "src-analysis", x = 0, y = 0, w = -1, h = -1}
		}
		parts.imageset = {}
		parts.value = {}
		parts.graph = {}

        parts.text = {
          {id = "subdiff",	font = "font-default-commonparts-sub", size = 24, align = 0, value = function() return display.subdiff end},
        }

        -- 表示切替用
        parts.customTimers = {
          {id = TIMER_SUBDIFF, timer = function()
            local display_song = {
              md5 = main_state.text(1030),
              sha256 = main_state.text(1031),
            }

            if now_song.md5 ~= display_song.md5
              then
                local subdiff = SUBDIFF_TABLE.md5[display_song.md5]
                if subdiff == nil then
                  subdiff = SUBDIFF_TABLE.sha256[display_song.sha256]
                end
                if subdiff ~= nil then
                  display.subdiff = subdiff
                  now_song.md5 = display_song.md5
                  now_song.sha256 = display_song.sha256
                end
                if now_song.md5 ~= display_song.md5 then
                  display.subdiff = "---"
                  now_song.md5 = display_song.md5
                  now_song.sha256 = display_song.sha256
                end
              end
            end}
          }

		parts.destination = {
          {
            id = "subdiff",
            dst = {
              {x = 380, y = 782, w = 544, h = 24},
            },
            -- timer = 11,
            -- loop = 300,
            -- dst = {
            --   {time = 0, x = 380, y = 812, w = 544, h = 24, acc=2, a= 0},
            --   {time = 300, y = 782, a = 255},
            -- },
          },
        }
	end
			
	return parts	
end

return {
	parts = parts,
	load = load
}
